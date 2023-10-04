from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import calinski_harabasz_score
from sklearn.naive_bayes import GaussianNB
from sklearn import cluster
import numpy as np
from matplotlib import colorbar
import xarray

class water:
        #fix
        required_bands = {'mndi','Green','ndwi','Mir2','mbwi'}
        required_indices = {'ndwi','mbwi','mndwi'}
        bands_keys = ['mndwi','ndwi','Mir2']
        invalid_mask = None
        glint_processor = None
        # config = config
        data_as_columns = None
        clusters_labels = None
        clusters_params = None
        cluster_matrix = None
        water_cluster = None
        water_mask = None
        best_k = None
        _product_name = None
        # bands_keys = bands_keys
        cluster_matrix = None
        train_size = 0.2
        min_train_size = 500
        max_train_size = 10000
        linkage = 'average'
        clip_band = ['mndwi', 'Mir2', 'ndwi']
        clip_inf_value = [-0.1, None, -0.15]
        clip_sup_value = [None, 0.075, None]
        glint_mode = True
        glint_processor = None
        detect_water_cluster = 'maxmndwi'
        min_k = 2
        score_index = 'calinsk'
        #unfix
        max_k = 5
        classifier = 'naivebayes'
        clustering_method = 'agglomerative'
        
        def __init__(self,dataset):
            # new
            if isinstance(dataset,xarray.core.dataset.Dataset):
                try:
                    red   = dataset.red.to_numpy()
                    green = dataset.green.to_numpy()
                    blue  = dataset.blue.to_numpy()
                    nir   = dataset.nir.to_numpy()
                    if 'swir1' in dataset.data_vars:
                        mir = dataset.swir1
                    elif 'swir_1' in dataset.data_vars:
                        mir = dataset.swir_1
                    else:
                        raise ValueError("Error to load swir1 band")
                    mir   = mir.to_numpy()
                    if 'swir2' in dataset.data_vars:
                        mir2 = dataset.swir1
                    elif 'swir_2' in dataset.data_vars:
                        mir2 = dataset.swir_1
                    else:
                        raise ValueError("Error to load swir2 band")
                    mir2   = mir2.to_numpy()
                except ValueError as e:
                    print(e)
                bands = {'Red':red,
                        'Green':green,
                        'Blue':blue,
                        'Nir':nir,
                        'Mir':mir,
                        'Mir2':mir2}
                dataset = bands
            # old
            self.input_bands = dataset
            bands = dict()
            for i,j in self.input_bands.items():
                quantize = j.squeeze()/10000
                bands.update({i:quantize})
            self.bands=bands

        def __str__(self):
            lst = list()
            for i in self.bands.keys():
                lst.append(i)
            lst = str(lst)
            return "bands : "+lst 
    
        def show(self):
            # oe.plotshow(oe.band_combination(self.bands['Red'],self.bands['Green'],self.bands['Blue'],5))
            print(self.bands)
            
        ############################################ DWImageClustering ############################################
        #check if the MNDWI index is necessary and if it exists
        @staticmethod
        def calc_normalized_difference(img1, img2, mask=None, compress_cte=0.02):
            """
            Calc the normalized difference of given arrays (img1 - img2)/(img1 + img2).
            Updates the mask if any invalid numbers (ex. np.inf or np.nan) are encountered
            :param img1         : first array
            :param img2         : second array
            :param mask         : initial mask, that will be updated
            :param compress_cte : amount of index compression. The greater, the more the index will be compressed towards 0
            :return             : nd array filled with -9999 in the mask and the mask itself
            """
            # create a minimum array
            min_values = np.where(img1 < img2, img1, img2)
            # then create the to_add matrix (min values turned into positive + epsilon)
            min_values = np.where(min_values <= 0, -min_values + 0.001, 0) + compress_cte
            nd = ((img1 + min_values) - (img2 + min_values)) / ((img1 + min_values) + (img2 + min_values))
            # Clipping value
            nd[nd > 1] = 1
            nd[nd < -1] = -1
            # https://github.com/olivierhagolle/modified_NDVI
            # if result is infinite, result should be 1
            nd[np.isinf(nd)] = 1
            # nd_mask = np.isinf(nd) | np.isnan(nd) | mask
            nd_mask = np.isnan(nd) | (mask if mask is not None else False)
            nd = np.ma.array(nd, mask=nd_mask, fill_value=-9999)
            return nd.filled(), nd.mask

        @staticmethod
        #check if the MBWI index exist
        def calc_mbwi(bands, factor, mask):
            # changement for negative SRE values scene
            min_cte = np.min([np.min(bands['Green'][~mask]), np.min(bands['Red'][~mask]),
                                np.min(bands['Nir'][~mask]), np.min(bands['Mir'][~mask]), np.min(bands['Mir2'][~mask])])
            if min_cte <= 0:
                min_cte = -min_cte + 0.001
            else:
                min_cte = 0
            mbwi = factor * (bands['Green'] + min_cte) - (bands['Red'] + min_cte) - (bands['Nir'] + min_cte) \
                    - (bands['Mir'] + min_cte) - (bands['Mir2'] + min_cte)
            mbwi[~mask] = RobustScaler(copy=False).fit_transform(mbwi[~mask].reshape(-1, 1)).reshape(-1)
            mbwi[~mask] = MinMaxScaler(feature_range=(-1, 1), copy=False).fit_transform(mbwi[~mask].reshape(-1, 1)) \
                .reshape(-1)
            mask = np.isinf(mbwi) | np.isnan(mbwi) | mask
            mbwi = np.ma.array(mbwi, mask=mask, fill_value=-9999)
            return mbwi, mask

        @staticmethod
        #check if the list contains the required bands
        def listify(lst, uniques=[]):
            # pdb.set_trace()
            for item in lst:
                if isinstance(item, list):
                    uniques = listify(item, uniques)
                else:
                    uniques.append(item)
            return uniques.copy()
        ############################################ DWImageClustering ############################################
        ############################################ run_detect_water #############################################
        #Transform the rasters in a matrix where each band is a column
        @staticmethod
        def bands_to_columns(bands,invalid_mask):
            """
            Convert self.bands to a column type matrix where each band is a column
            It follows the order of the keys ordered
            :return : column type matrix
            """
            data = None
            for key in sorted(bands.keys()):
                band_array = bands[key]

                band_as_column = band_array[~invalid_mask].reshape(-1,1)

                if (key == 'Mir') or (key == 'Mir2') or (key == 'Nir') or (key == 'Nir2') or (key == 'Green'):
                    band_as_column = band_as_column * 4
                    band_as_column[band_as_column > 4] = 4

                data = band_as_column if data is None else np.concatenate([data, band_as_column], axis=1)
            return data

        # if algorithm is not kmeans,split data for a smaller ser (for performnce purposes)
        @staticmethod
        def get_train_test_split(data,train_size,min_train_size,max_train_size):
            """
            Split the provided data in train-test bunches
            :param min_train_size : minimum data quantity for train set
            :param max_train_size : maximum data quantity for train set
            :param train_size     : percentage of the data to be used as train dataset
            :param data           : data to be split
            :return               : train and test datasets
            """
            dataset_size = data.shape[0]

            if (dataset_size * train_size) < min_train_size:
                train_size = min_train_size / dataset_size
                train_size = 1 if train_size > 1 else train_size

            elif (dataset_size * train_size) > max_train_size:
                train_size = max_train_size / dataset_size
            
            return train_test_split(data, train_size=train_size)
        
        #create data bunch only with the bands used for clustering
        @staticmethod
        def split_data_by_bands(bands,data, selected_keys):
            """
            Gets data in column format (each band is a column) and returns only the desired bands
            :param data          : data in column format
            :param selected_keys : bands keys to be extracted
            :return              : data in column format only with the selected bands
            """
            bands_index = []
            bands_keys = list(sorted(bands.keys()))

            for key in selected_keys:
                bands_index.append(bands_keys.index(key))
            return data[:, bands_index]
        
    
        def find_best_k(self,data):
            """
            Find the best number of clusters according to an metrics.
            :param data : data to be tested
            :return     : number of clusters
            """
            # print('min_k :',self.min_k)
            # print('max_k :',self.max_k)
            # print('score_index :',self.score_index)
            # print(data)

            if self.min_k == self.max_k:
                print('Same number for minimum and maximum clusters: k = {}'.format(self.min_k))
                best_k = self.min_k
                return best_k

            # if score_index == 'silhouette':
            #     print('Selection of best number of clusters using Silhouete Index:')
            # else:
            #     print('Selection of best number of clusters using Calinski-Harabasz Index:')

            # if self.score_index == 'silhouette':
            #     print('score_index --> Silhouete')
            # else:
            #     print('score_index --> Calinski_harabaz')

            computed_metrics = []
            for num_k in range(self.min_k, self.max_k + 1):
                # cluster_model = cluster.KMeans(n_clusters=num_k, init='k-means++')
                cluster_model = cluster.AgglomerativeClustering(n_clusters=num_k, linkage=self.linkage)

                labels = cluster_model.fit_predict(data)

                if self.score_index == 'silhouette':
                    computed_metrics.append(metrics.silhouette_score(data, labels))
                    # print('k = {} index : {}'.format(num_k, computed_metrics[num_k - self.min_k]))

                else:
                    computed_metrics.append(calinski_harabasz_score(data, labels))
                    # print('k = {} index : {}'.format(num_k, computed_metrics[num_k - self.min_k]))

            best_k = computed_metrics.index(max(computed_metrics)) + self.min_k
            # print("best_k :",best_k)

            return best_k
        
        #apply the clusterization algorithm and return labels and train dataset
        @staticmethod
        def apply_cluster(data,best_k):
            """
            Apply the cluster algorithm to the data. Number of cluster is in self.best_k
            :param data  : data to be clustered
            :return      : Vector with the labels
            """
            clustering_method = 'agglomerative'
            if clustering_method == 'kmeans':
                cluster_model = cluster.KMeans(n_clusters=best_k, init='k-means++')
            elif clustering_method == 'gauss_mixture':
                cluster_model = GMM(n_components=best_k, covariance_type='full')
            else:
                cluster_model = cluster.AgglomerativeClustering(n_clusters=best_k, linkage='average')

            cluster_model.fit(data)
            return cluster_model.labels_.astype('int8')
        
        #cals statistics for each cluster
        @staticmethod
        def calc_clusters_params(data, clusters_labels,best_k):
            """
            Calculate parameters for each encountered cluster.
            Mean, Variance, Std-dev
            :param data            : Clustered data
            :param clusters_labels : Labels for the data
            :return                : List with cluster statistics
            """
            clusters_params = []
            for label_i in range(best_k):
                # first slice the values in the indexed cluster
                cluster_i = data[clusters_labels == label_i, :]

                cluster_param = {'clusterid': label_i}
                cluster_param.update({'mean': np.mean(cluster_i, 0)})
                cluster_param.update({'variance': np.var(cluster_i, 0)})
                cluster_param.update({'stdev': np.std(cluster_i, 0)})
                cluster_param.update({'diffb2b1': cluster_param['mean'][1] - cluster_param['mean'][0]})
                cluster_param.update({'pixels': cluster_i.shape[0]})

                clusters_params.append(cluster_param)

            return clusters_params
        
        #detect the water cluster
        @staticmethod
        def detect_cluster(bands,clusters_params, param, logic, band1, band2=None):
            """
            Detects a cluster according to a specific metrics
            :param param : Which parameter to search (mean, std-dev, variance,  ...)
            :param logic : Max or Min
            :param band1 : The band related to the parameter
            :param band2 :
            :return      : Cluster object that satisfies the logic
            """
            # get the bands available in the columns
            available_bands = sorted(bands.keys())

            param_list = []
            if band1:
                idx_band1 = available_bands.index(band1)
            if band2:
                idx_band2 = available_bands.index(band2)

            # todo: fix the fixed values
            for clt in clusters_params:
                if param == 'diff':
                    if not idx_band2:
                        raise OSError('Two bands needed for diff method')
                    param_list.append(clt['mean'][idx_band1] - clt['mean'][idx_band2])

                elif param == 'value':
                    if (clt['pixels'] > 5): # and (clt['mean'][available_bands.index('Mir2')] < 0.25*4):
                        param_list.append(clt['mean'][idx_band1])
                    else:
                        param_list.append(-1)

            if logic == 'max':
                idx_detected = param_list.index(max(param_list))
            else:
                idx_detected = param_list.index(min(param_list))

            return clusters_params[idx_detected]
        
        def identify_water_cluster(self,detect_water_cluster,bands):
            """
            Finds the water cluster within all the clusters.
            It can be done using MNDWI, MBWI or Mir2 bands
            :return: water cluster object
            """
            if detect_water_cluster == 'maxmndwi':
                if 'mndwi' not in bands.keys():
                    raise OSError('MNDWI band necessary for detecting water with maxmndwi option')
                water_cluster = self.detect_cluster(bands,self.clusters_params,'value', 'max', 'mndwi')

            # elif detect_water_cluster == 'maxmbwi':
            #     if 'mbwi' not in bands.keys():
            #         raise OSError('MBWI band necessary for detecting water with maxmbwi option')
            #     water_cluster = detect_cluster(bands,clusters_params,'value', 'max', 'mbwi')

            # elif detect_water_cluster == 'minmir2':
            #     if 'mndwi' not in bands.keys():
            #         raise OSError('Mir2 band necessary for detecting water with minmir2 option')
            #     water_cluster = detect_cluster(bands,clusters_params,'value', 'min', 'Mir2')

            # elif detect_water_cluster == 'maxndwi':
            #     if 'ndwi' not in bands.keys():
            #         raise OSError('NDWI band necessary for detecting water with minmir2 option')
            #     water_cluster = detect_cluster(bands,clusters_params,'value', 'max', 'ndwi')

            # elif detect_water_cluster == 'minnir':
            #     water_cluster = detect_cluster(bands,clusters_params,'value', 'min', 'Nir')

            # else:
            #     raise OSError('Method {} for detecting water cluster does not exist'.
            #                     format(self.config.detect_water_cluster))

            return water_cluster
        
        @staticmethod
        def apply_naive_bayes(data, clusters_labels, clusters_data):
            """
            Apply Naive Bayes classifier to classify data
            :param data            : new data to be classified
            :param clusters_labels : labels for the reference data
            :param clusters_data   : reference data
            :return                : labels for the new data
            """
            # train a NB classifier with the data and labels provided
            model = GaussianNB()

            # print('Applying clusters based --> naive bayes classifier')
            # print('Cross_val_score:{}'.format(cross_val_score(model, clusters_data, clusters_labels)))

            model.fit(clusters_data, clusters_labels)

            # return the new predicted labels for the whole dataset
            return model.predict(data)
        
        
        def supervised_classification(self,data, train_data, clusters_labels):
            """
            Applies a machine learning supervised classification
            :param data            : new data to be classified
            :param train_data      : reference data
            :param clusters_labels : labels for the reference data
            :return                : labels for the new data
            """
            if self.classifier == 'SVM':
                clusters_labels = apply_svm(data, clusters_labels, train_data)
            elif self.classifier == 'MLP':
                clusters_labels = apply_mlp(data, clusters_labels, train_data)
            else:
                clusters_labels = self.apply_naive_bayes(data, clusters_labels, train_data)

            return clusters_labels.astype('int8')
        
        # after obtain the final labels,clip bands with superios limit
        # after obtainting the final labels,clip bands with inferior limit
        #create an cluster array based on the cluster result (water will be value1)
        @staticmethod
        def create_matrice_cluster(indices_array,bands,clusters_labels,water_cluster,best_k):
            """
            Recreates the matrix with the original shape with the cluster labels for each pixel
            :param indices_array : position of the clustered pixels in the matrix
            :return              : clustered image (0-no data, 1-water, 2, 3, ... - other)
            """
            # create an empty matrix
            matrice_cluster = np.zeros_like(list(bands.values())[0]).astype('int8')

            # apply water pixels to value 1
            matrice_cluster[indices_array[0][clusters_labels == water_cluster['clusterid']],
                            indices_array[1][clusters_labels == water_cluster['clusterid']]] = 1

            # print('Assgnin 1 to cluster_id {}'.format(water_cluster['clusterid']))

            # loop through the remaining labels and apply value >= 3
            new_label = 2
            for label_i in range(best_k):

                if label_i != water_cluster['clusterid']:
                    matrice_cluster[indices_array[0][clusters_labels == label_i],
                                    indices_array[1][clusters_labels == label_i]] = new_label

                    new_label += 1
                else:
                    pass
                    # print('Skipping cluster_id {}'.format(label_i))

            return matrice_cluster


        ################################################ waterdetection #################################################
        def waterdetect(self):
            """
            waterdetection
            :return : watermask
            """
            ## wd.DWImageClustering
            # get the first band as reference of size
            ref_band = list(self.bands.keys())[0]
            ref_shape = self.bands[ref_band].shape

            #check the invalid_mask
            invalid_mask = np.zeros(ref_shape,dtype=bool)
            
            #check if the MNDWI index is necessary and if it exists
            if 'mndwi' in self.required_indices and 'mndwi' not in self.bands:
                mndwi,mndwi_mask = self.calc_normalized_difference(self.bands['Green'],self.bands['Mir2'],invalid_mask)
                invalid_mask |= mndwi_mask
                self.bands.update({'mndwi':mndwi})

            #check if the NDWI index exist
            if 'ndwi' in self.required_bands and 'ndwi' not in self.bands.keys():
                ndwi,ndwi_mask = self.calc_normalized_difference(self.bands['Green'],self.bands['Nir'],invalid_mask)
                invalid_mask |= ndwi_mask
                self.bands.update({'ndwi':ndwi})

            #check if the MBWI index exist
            if 'mbwi' in self.required_bands and 'mbwi' not in self.bands.keys():
                mbwi,mbwi_mask = self.calc_mbwi(self.bands,3,invalid_mask)
                invalid_mask |= mbwi_mask

            #check if the list contains the required bands
            for band in self.listify(self.bands_keys):
                if band == 'otsu' or band == 'canny':
                    continue
                if band not in self.bands.keys():
                    raise OSError('Band {}, not available in the dictionary'.format(self.band))
                if type(self.bands[band]) is not np.ndarray:
                    raise OSError('Band {} is not a numpy array'.format(self.band))
                if ref_shape != self.bands[band].shape:
                    raise OSError('Bands {} and {} with different size in clustering core'.format(self.band, ref_band))
                else:
                    pass
                    # print("band : ",band+"In require bands list")

            ## run_detect_water
            # print('My.DataComponent : self.bands_keys[0] :',self.bands_keys[0])
            #if passed options,override the existing options
            if self.bands_keys[0] == 'otsu':
                cluster_matrix = self.apply_otsu_treshold()
            elif self.bands_keys[0] == 'canny':
                cluster_matrix = self.apply_canny_treshold()
            elif False:
                cluster_matrix = None

            #Transform the rasters in a matrix where each band is a column
            data_as_columns = self.bands_to_columns(self.bands,invalid_mask)

            # two line vectors indicating the indexes (line column) of valid pixels
            ind_data = np.where(~invalid_mask)   

            # if algorithm is not kmeans,split data for a smaller ser (for performnce purposes)
            if self.clustering_method == 'kmean':
                train_data_as_columns=data_as_columns
            else:
                train_data_as_columns,ts= self.get_train_test_split(data_as_columns,self.train_size,self.min_train_size,self.max_train_size)

            #split1
            split_train_data_as_columns = self.split_data_by_bands(self.bands,train_data_as_columns,self.bands_keys)
            #split2
            split_data_as_columns = self.split_data_by_bands(self.bands,data_as_columns,self.bands_keys)

            #find best_k
            best_k = self.find_best_k(split_train_data_as_columns)

            #apply the clusterization algorithm and return labels and train dataset
            train_clusters_labels = self.apply_cluster(split_train_data_as_columns,best_k)

            #cals statistics for each cluster
            self.clusters_params = self.calc_clusters_params(train_data_as_columns,train_clusters_labels,best_k)

            #detect the water cluster
            water_cluster = self.identify_water_cluster(self.detect_water_cluster,self.bands)

            if self.clustering_method != 'kmeans':
                clusters_labels = self.supervised_classification(split_data_as_columns,split_train_data_as_columns,train_clusters_labels)
            else:
                clusters_labels = train_clusters_labels
            # print('My.DataComponent : clusters_labels :',clusters_labels)
            # after obtain the final labels,clip bands with superios limit
            for band,value in zip(self.clip_band,self.clip_sup_value):
                if value is not None:
                    if self.glint_mode and self.glint_processor is not None:
                        print('0')
                    else:
                        comp_array = value
                    clusters_labels[(clusters_labels == water_cluster['clusterid']) & (self.bands[band][~invalid_mask]>comp_array)] = -1
            #after obtainting the final labels,clip bands with inferior limit
            for band,value in zip(self.clip_band,self.clip_inf_value):
                if value is not None:
                    if self.glint_mode and self.glint_processor is not None:
                        print('0')
                    else:
                        comp_array = value
                    clusters_labels[(clusters_labels == water_cluster['clusterid']) & (self.bands[band][~invalid_mask]<comp_array)] = -1
            
            #create an cluster array based on the cluster result (water will be value1)
            cluster_matrix = self.create_matrice_cluster(ind_data,self.bands,clusters_labels,water_cluster,best_k)
            water_mask = np.where(cluster_matrix == 1,1,np.where(invalid_mask == 1,255,0)).astype('int8')
            watermask0 = water_mask==0
            watermask1 = water_mask==1
            return watermask1

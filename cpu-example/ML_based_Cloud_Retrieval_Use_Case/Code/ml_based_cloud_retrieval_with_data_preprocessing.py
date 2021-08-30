import sys
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import joblib
import time
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import tables
import glob
import os
import h5py
from datetimerange import DateTimeRange

# common_path = '/content/drive/Shareddrives/ML_Capacity_Development_ESDSWG/ML_Capacity_Development_ESDSWG/ML_based_Cloud_Retrieval_Use_Case/'
common_path = '../'
general_lib_path = common_path + 'Code'
import sys
sys.path.insert(1,general_lib_path)
import instrument_reader as ir
import general_collocation as gc

def ml_process():
  """#Data collocation based on time and location
  It collocates CALIPSO and VIIRS data, and save collocated data into seperate h5 files
  """

  #collocate caliop with viirs
  maximum_distance = 5.0  #kilometer
  maximum_interval = 15.0 #minute
  viirs_resolution = 0.75 #kilometer

  clayer1km_path = common_path + 'Data/raw_data/CALIPSO-L2-01km-CLayer/'
  vnp02_path = common_path + 'Data/raw_data/VNP02MOD-VIIRS-Attributes/'
  vnp03_path = common_path + 'Data/raw_data/VNP03MOD-VIIRS-Coordinates/'
  save_path = common_path + 'Data/intermediary_output/'

  clayer1km_files = sorted(glob.glob(clayer1km_path+'*01-01*.hdf'))
  vnp03_files = sorted(glob.glob(vnp03_path+'*.nc'))
  vnp_timeranges = gc.get_modis_viirs_timerange(vnp03_files)
  print ("111",vnp03_files)

  #collocation main logic
  collocated_vnp02_files = []
  collocated_caliop_files = []
  for clayer1km_file in clayer1km_files:

      print ("222",clayer1km_file)
      cal_name = os.path.basename(clayer1km_file)
      pos = cal_name.find('V4-10.')
      cal_timeflag = cal_name[pos+6:pos+27]
      print ("333",cal_timeflag)

      clayer1km_geo = ir.load_caliop_clayer1km_geoloc(cal_1km_file=clayer1km_file)
      caliop_dts = clayer1km_geo['Profile_Datetime']
      caliop_timerange = DateTimeRange(caliop_dts[0],caliop_dts[-1])
      overlap_flags = gc.find_overlap( caliop_timerange, vnp_timeranges )
      indices = np.where(overlap_flags==1)[0]
      print (indices)

      for index in indices:

          print ('Find collocation pixels for:')
          print ('File 1:', cal_name)
          print ('File 2:', os.path.basename(vnp03_files[index]))

          vnp03_name = os.path.basename(vnp03_files[index])
          pos = vnp03_name.find('.A')
          vnp_timeflag = vnp03_name[pos+2:pos+14]
          vnp02_files = glob.glob(vnp02_path+'*'+vnp_timeflag+"*.nc")


          clayer1km_geo = ir.load_caliop_clayer1km_geoloc(cal_1km_file=clayer1km_file)
          vnp_geo = ir.load_viirs_vnp03_geoloc(vnp03_file=vnp03_files[index])

          caliop_lat = clayer1km_geo['Latitude']
          caliop_lon = clayer1km_geo['Longitude']
          caliop_dts = clayer1km_geo['Profile_Datetime']

          viirs_lat = vnp_geo['Latitude']
          viirs_lon = vnp_geo['Longitude']
          viirs_dt  = vnp_geo['Datetime'][1]

          collocation_indexing = gc.track_swath_collocation(track_lat=caliop_lat, track_lon=caliop_lon, track_time=caliop_dts,
                                swath_lat= viirs_lat, swath_lon= viirs_lon, swath_time= viirs_dt,
                                swath_resolution=viirs_resolution,
                                maximum_distance=maximum_distance, maximum_interval=maximum_interval)

          caliop_ind = collocation_indexing['track_index_x']
          if ( len(np.where(caliop_ind>=0)[0])<=1 ):
              print ( 'No collocate pixel found' )
              print ( '' )
              continue
          else:
              n_col =  len(np.where(caliop_ind>=0)[0])
              print("Collocated pixels: %5d" % n_col)
              print ( '' )

          #save calipso-viirs collocation indexing data
          sav_name = 'CAL_' + cal_timeflag + '_VNP_' + vnp_timeflag + '_Index.h5'
          sav_id = h5py.File(save_path+sav_name,'w')
          sav_id.create_dataset('CALIPSO_Track_Index',data=collocation_indexing['track_index_x'])
          sav_id.create_dataset('VIIRS_CrossTrack_Index',data=collocation_indexing['swath_index_y'])
          sav_id.create_dataset('VIIRS_AlongTrack_Index',data=collocation_indexing['swath_index_x'])
          sav_id.create_dataset('CALIPSO_VIIRS_Distance',data=collocation_indexing['swath_track_distance'])
          sav_id.create_dataset('CALIPSO_VIIRS_Interval',data=collocation_indexing['swath_track_time_difference'])
          sav_id.close()

          #save calipso-viirs collocation data
          #code for saving calipso Level 1/2 data
          #input:
          #calipso_file : CALIPSO L1 or L2 file
          #calipso_index : Indices of CALIPSO profiles that are collocated with viirs 
          #selected_datasets : list of dataset names that need to be saved
          sav_name = 'CAL_' + cal_timeflag + '_VNP_' + vnp_timeflag + '_CALIOP_CLayer1km.h5'
          #get label from calipso
          calipso_datasets = ['Longitude','Latitude','Layer_Top_Temperature','Layer_Top_Pressure','IGBP_Surface_Type','Snow_Ice_Surface_Type','Number_Layers_Found','Feature_Classification_Flags']
          ir.save_caliop_dataset(calipso_file=clayer1km_file,calipso_index=caliop_ind,selected_datasets=calipso_datasets,save_file=save_path+sav_name)
          collocated_caliop_files = np.append(collocated_caliop_files, save_path+sav_name)

          sav_name = 'CAL_' + cal_timeflag + '_VNP_' + vnp_timeflag + '_VIIRS_L1b.h5'
          #viirs_03_datasets = ['/geolocation_data/latitude','/geolocation_data/longitude']
          #viirs 02 data to get its 16 bands
          viirs_02_datasets = ['/observation_data/M01', '/observation_data/M02', '/observation_data/M03', '/observation_data/M04','/observation_data/M05', '/observation_data/M06', '/observation_data/M07', '/observation_data/M08','/observation_data/M09', '/observation_data/M10', '/observation_data/M11', '/observation_data/M12','/observation_data/M13', '/observation_data/M14', '/observation_data/M15', '/observation_data/M16']
          ir.save_viirs_dataset(viirs_file=vnp02_files[0],viirs_along=collocation_indexing['swath_index_x'],
                                viirs_cross=collocation_indexing['swath_index_y'],selected_datasets=viirs_02_datasets,save_file=save_path+sav_name)
          collocated_vnp02_files = np.append(collocated_vnp02_files, save_path+sav_name)
      #break

  """# Set labels and features
  Use CALIPSO as Feature_Classification_Flags attribute values as labels.

  Use VIIRS 16 bands as features.

  """

  # read Feature_Classification_Flags attribute and its 6 and 7 binary digits from right to retrieve cloud phases as value in [0, 3]
  np_caliop = []
  for collocated_caliop_file in collocated_caliop_files:
      h5_caliop = h5py.File(collocated_caliop_file, 'r')
      np.set_printoptions(threshold=np.inf)
      #print(np.array(h5_caliop['/Feature_Classification_Flags'][:,0]))
      np_caliop = np.append(np_caliop, (np.array(h5_caliop['/Feature_Classification_Flags'][:,0], dtype = "byte") & 0b0000000011000000) >> 6)
      #print(np_caliop)

  #print(np_caliop.shape)

  # read 16 bands from VIIRS data as features

  df_vnp02 = pd.DataFrame([])
  df_vnp02_individual = pd.DataFrame([])
  df_vnp02_cols = ["M{:02d}".format(b) for b in range(1,17)]
  for collocated_vnp02_file in collocated_vnp02_files:
      h5_vnp02 = h5py.File(collocated_vnp02_file, 'r')
      for index in df_vnp02_cols:
          #print(h5_vnp02.get('/observation_data/'+index)[:].shape)
          df_vnp02_individual = df_vnp02_individual.append(pd.Series(h5_vnp02.get('/observation_data/'+index)[:]), ignore_index=True)
      print(df_vnp02_individual.shape)
      df_vnp02 = df_vnp02.append(df_vnp02_individual.T, ignore_index=True)
      df_vnp02_individual = pd.DataFrame([])
      #print(df_vnp02.shape)
  df_vnp02.columns = df_vnp02_cols
  print(df_vnp02)

  # separate the data set into two parts (training 70% and testing 30%)
  testing_size = 0.30
  seed = 7
  train_X, test_X, train_Y, test_Y = model_selection.train_test_split(df_vnp02.values,np_caliop,test_size=testing_size,random_state=seed)

  # check the size of training and testing parts
  print(train_X.shape,train_Y.shape)
  print(test_X.shape, test_Y.shape)

  """#Random Forest based Machine Learning Model Training"""

  #Define Random Forest parameters
  n_estimators = 150
  max_depth = 15
  bootstrap = True
  criterion = 'entropy'
  class_weight = None
  random_state = 123456
  n_job = -1

  rfforest = RandomForestClassifier(n_estimators=n_estimators, bootstrap=bootstrap, criterion=criterion,
                                    max_depth=max_depth, oob_score=False,
                                    class_weight=class_weight, random_state=random_state, n_jobs=n_job)
  print ('Training RandomForest')
  rfforest.fit(train_X,train_Y.ravel())

  print('Training Data Performance')
  train_predict_Y = rfforest.predict(train_X)
  train_predict_YP = rfforest.predict_proba(train_X)
  print(accuracy_score(train_Y, train_predict_Y))

  print('Testing Data Performance')
  test_predict_Y = rfforest.predict(test_X)
  test_predict_YP = rfforest.predict_proba(test_X)
  print(accuracy_score(test_Y, test_predict_Y))

  """#Save Trained Model"""

  # save trained model
  joblib.dump(rfforest, '../Model/raw-data.model')

  # # load existing model
  # rfforest = joblib.load('../Model/raw-data.model')

  # """#Check Feature Importance, Data Distribution and Confusion Matrix based on Trained Model"""

  # # show feature importance:
  # feature_names = np.array(["M{:02d}".format(b) for b in range(1,17)])
  # tree_importance_sorted_idx = np.argsort(rfforest.feature_importances_)
  # tree_indices = np.arange(0, len(rfforest.feature_importances_)) + 0.5
  # fig, (ax1) = plt.subplots(1, 1, figsize=(12, 8))
  # ax1.barh(tree_indices,
  #          rfforest.feature_importances_[tree_importance_sorted_idx], height=0.7)
  # ax1.set_yticklabels(feature_names[tree_importance_sorted_idx])
  # ax1.set_yticks(tree_indices)
  # ax1.set_ylim((0, len(rfforest.feature_importances_)))

  # fig.tight_layout()
  # plt.show()

  # #show probability distribution functions
  # fig, (ax1,ax2,ax3) = plt.subplots(3, 1, figsize=(12, 12))
  # sns.distplot(test_predict_YP[:,0],ax=ax1); # clear sky probability
  # sns.distplot(test_predict_YP[:,1],ax=ax2); # Ice Cloud probability
  # sns.distplot(test_predict_YP[:,2],ax=ax3); # Liquid Water Cloud probability
  # ax1.set_title('Clear Sky Probability Distribution')
  # ax2.set_title('Ice Cloud Probability Distribution')
  # ax3.set_title('Liquid Water Cloud Probability Distribution')

  # def plot_confusion_matrix(cm, classes,
  #                           normalize=False,
  #                           title='Confusion matrix',
  #                           cmap=plt.cm.Blues):
  #     """
  #     This function prints and plots the confusion matrix.
  #     Normalization can be applied by setting `normalize=True`.
  #     """
  #     import itertools
  #     if normalize:
  #         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
  #         print("Normalized confusion matrix")
  #     else:
  #         print('Confusion matrix, without normalization')

  #     print(cm)

  #     fig, (ax1) = plt.subplots(1, 1, figsize=(8, 8))

  #     plt.imshow(cm, cmap=cmap)
  #     plt.title(title)
  #     plt.colorbar()
  #     tick_marks = np.arange(len(classes))
  #     plt.xticks(tick_marks, classes, rotation=45, size=15)
  #     plt.yticks(tick_marks, classes, size=15)

  #     fmt = '.2f' if normalize else 'd'
  #     thresh = cm.max() / 2.
  #     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
  #         plt.text(j, i, format(cm[i, j], fmt),
  #                 horizontalalignment="center",
  #                 color="white" if cm[i, j] > thresh else "black", size=15)

  #     plt.ylabel('True label',size=15)
  #     plt.xlabel('Predicted label',size=15)
  #     plt.ylim([-0.5,-0.5+len(classes)])
  #     plt.tight_layout()

  # #show confusion matrix
  # CM = confusion_matrix(test_Y, test_predict_Y)

  # plot_confusion_matrix(CM, classes=['Clear', 'Ice', 'Liq'],
  #                       title='Confusion matrix, without normalization')
  # plt.show()

if __name__ == "__main__":

    start = time.time()
    ml_process()
    end = time.time()

    print("Done. Execution time = ", end - start, " s")
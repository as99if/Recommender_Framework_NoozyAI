

install requirements in environment
-
env: python 3.7
IDE: PyCharm 2021

Process:
---
* Input: review .src/recommender_algorithm_input.yml
    
    description - yaml
    
        input:
          description:
            - "algorithm_id: required"
            - "n: required"
            - "user_id_requirement: 'optional'(default)"
            - "video_id_requirement: 'required' / 'optional' / 'not required' (default)"
            - "dependant_data_parameters - a list of needed parameters for analysis (required)"
          # name of the algorithm module (.src/algorithm/random_basic.py)
          algorithm_id : "random_basic"
          n: 5
          user_id_requirement: "optional"
          # user_id_requirement: - only required for content based / optional for item based algorithm
          video_id_requirement: "not required"
          # dependant_data_parameters eg. 'dc:description' OR 'dc:available'
          dependant_data_parameters : ['dc:identifier', 'dc:available', 'dc:created']
          start_from :
            day: 1
            month: 1
            year: 2021





* Data collect:
    Metadata:
        
        {
            'dc:title': Title of the Video,
            'dc:identifier': Hash Key or Identifier,
            'dc:subject': (Theme)
                {
                    'identifier': Subject Identifier,
                    'title': Subject of the Video
                },
            'dc:description': Description of the Video
            'dc:publisher':
                {
                    'identifier': Publisher Identifier
                    'title': Publisher Name (eg. Vosges TV, Alsace 20, MoselleTV, Canal32, etc.),
                },
            'dc:contributor':
                {
                    'identifier': Contributor Identifier,
                    'title': Contributor Name (eg. Vosges TV, Canal 32, Pylprod, Mara Films, etc.),
                },
            'dc:created': Creation Date of the Video,
            'dc:modified': Modification Date of the Video,
            'dc:available': Availability Date of the Video,
            'dc:extent': Total Duration of the Video,
            'dc:type': (Genre)
                {
                    'identifier': Genre Identifier,
                    'title': Genre Name,
                },
            'dc:licence': Licence of the Video (eg. Free),
            'dc:audience': Audience of the Video (eg. National, Department, Region),
            'dc:rightsHolder':
                {
                    'identifier': Rights Holder,
                    'title': Rights Holder Name,
                },
            'dc:coverage': (Latitude, Longitude) coordinates,
            'dc:source.identifier': Source Identifier of the Video,
            'dc:source.title': Source Title of the Video
        }

Pre-process : Utilities (below)

Algorithm process

Post-process: Utilities (below)

Output: .src/results/ .json (and also stores into redis repository)

json result file's data structure:
Particular for only this algorithm module and separate result json file.

      {
        "recommendation_results": [
          {
            "user_id": "None",
            "random_basic": [
              {
                "header": {
                  "algorithm_id": "random_basic",
                  "N": 5,
                  "user_id": null,
                  "video_id": null,
                  "timestamp": 1622560963.032463,
                },
                "result": [
                  {
                    "video_id": "ewlXMHfWmr",
                    "rank": 1,
                    "score": 1.0
                  },
                  {
                    "video_id": "20rm417J4O",
                    ..
                  },
                  {
                    ..
                  }
                ]
              }
            ]
          },
          {
            "user_id": "10306994",
            "random_basic": [
              {
                "header": {
                     ...
                  },
                "result": [
                  {
                    "video_id": "mbWnmZ2Rjc",
                    "score": 0.19999999999999996

                     ...
                  }
                ]
              }
            ]
          },
          {
            "user_id": "9492917",
            "random_basic":
          },
          .....
        ],
        "process_start_timestamp": 1622560963.0188391,
        "process_finish_timestamp": 1622560963.241937
      }


** All the algorithm modules will be connected to a single 'result_redis' db/repository.

** Where, KEY is 'user_id' . For unauthorized user, user_id = 'null' / None. 

** When the Recommender Engine (API gateway) requests, it will get value[user_id][algorithm_id], and then process and get recommendation results.

result_redis structure:

root/

      - {user_id[0]}:
         - {algorithm_id} eg:
         - "random_basic":
            - "user_id": {user_id[0]}
            - "header":
               - "algorithm_id": random_basic
               - "N": 5
               - "user_id": null
               - "video_id": null
               - "timestamp": 1622560963.032463
            - "results"
               - [
                  - video {"video_id", "rank", "score"}
                  - video
                  - video
                  ........
                  ]
         - "content_based":
            - "header":
            - "results":
         - "most_popular":
            - "header":
            - "results":
         - "most_recent":
            - "header"
            - "results"
         - "collaborative_filtering":
            - "header":
            - "results":
         - ......
      - {user_id[1]}
         - ...
      - {user_id[2]}
      - ..
      - {user_id[n]}
   
user_id[0] = null OR None

Add algorithm
--
project name: recommender-[algorithm-name]-algorithm

    
1. Develop algorithm,
   
    In directory ./src/algorithm/

    * create the  [algorithm_id].py

    * create a module (not class) with recommend() and get_recommendation() method implemented.

    (eg. same as algorithm_template.py or random_basic.py)

   ** All the pre-process and post-process in done in ".src/recommender/" directory.
   ** This algorithm_id.py module will take dataframe (df_videos, df_stats, merged_data, view_matrix, etc) and will return dataframe (resulting video hash_keys).
   

Edit .src/Dockerfile
        
            # * change the latter part with algorithm module name 
            COPY ../src/requirements.txt /usr/src/noozy_recommender_template/
    
            # * change the latter part with algorithm module name 
            # don't need this line if taken from git
            COPY . /usr/src/noozy_recommender_template
            Build Docker image and Run container

TODO: have to do

Build Docker image and Run container        
--
            make build
            make up


---

OR

Standalone run
--
later to be added to scheduler

        virtualenv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python src/recommender_algorithm_run.py


Configuration file
--
.src/config/noozy.ini


Utilities
--
.src/algorithm/utils.py

   
   pre-process : 
      
      clean metadata : metadata_clean()
      clean xapi statements: xapi_data_clean()
      merging xapi and metadata : merge()
      creating view matrix : create_view_matrix()
      creating similarity matrix
   
   post-process : 
      
      post_process: post_process()
      filtering by user : filter_videos_per_user()
      format result : get_result()

Recommender process handle
--
.src/recommender/noozy_recommender.py

Metadata
--
.src/recommender/noozy_metadata_client/

Xapi statements
--
.src/recommender/noozy_xapi_client/

Result store
---
.src/recommender/noozy_result_client/

   - .src/recommender/noozy_result_client/noozy_recommendation_store.py

         - append_item(): append receommendation into the result list in a formatted way
         - put_item(): put receommendation item according to item[user_id][algorithm_id] in redis db
         - result_store(): stores this modules result in a json file in .src/results/
         


TODO:
---
Store in redis (in progress)
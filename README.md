PubMed Random Retrieval
========================

This library download abstracts in an Random manner.


========================

1.- Clone this repository 

    $ git clone https://github.com/javicorvi/pubmed_random_retrieval.git
    
2.- Python 2.7 
	
	
3.- Third Party 
	
		
4.- Run the script
	
	To run the script just execute python pubmed_random_retrieval -p /home/myuser/config.properties
	
	The config.properties file contains the parameters for the execution
	
	[MAIN]
	output=/home/user/output_folder
	quantity=1000
	start=1
	end=50000000
	
	
	The output is the directory in wich the pubmed articles will be downloaded in xml format.
	quantity is the number of pubmed abstract that will be downloaded.
	star and end are the boundaries of the pmid abstract to be downloaded.
		
5.- The container 
	
	If you just want to run the app without any kind of configuration you can do it 
	through the docker container is avaiblable in https://hub.docker.com/r/inab/pubmed_random_retrieval/ 

	The path home/yourname/your_work_dir will be the working directory in where the data will be downloaded, this is the configuration of a 
	Volumes for stored the data outside of the container and then standardized by this container.

	To run the docker: 
	
	1)  Wiht the default parameters: 
	    
	    docker run --rm -u $UID  -v /home/yourname/your_work_dir/:/app/data pubmed_random_retrieval python pubmed_random_retrieval.py -p config.properties

		The default config.properties its inside the container and has the following default parameters: 
		
		[MAIN]
		output=/home/user/output_folder
		quantity=1000
		start=1
		end=50000000
	
	2) Passing specific config.properties file:
	
		Put your own config file in the your working directory:  /home/yourname/your_work_dir/config.properties  
		
		docker run --rm -u $UID  -v /home/yourname/your_work_dir/:/app/data pubmed_standardization python pubmed_standardization.py -p /app/data/config_own.properties
		
		
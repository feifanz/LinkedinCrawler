# LinkedinCrawler
LinkedinCrawler can automatically collect basic Linkedin profiles and perform cluster algorithm on them.
Separation of front and rear ends:
   - The front-end based on react framework and ant design ui
   - The back-end based on flask framework
   - Also Need Chrome browser and chromedriver to support the Crawler module

# Modules
1. Modules
1) Crawler module, can automatically collect Linkedin profile. 
   Can set parameters at '/Users/feifanzhang/LinkedinCrawler/server/crawler/parameters.py'
   
2) Cluster module, using k-means algorithm to cluster the data, there are two ways to choose features:
   - The number of job description, he number of connection
   - The text content of job description, use TF-IDF deal with it

2. Test the module
There are test scripts provided in '/Users/feifanzhang/LinkedinCrawler/server/test'
Run 'python test_crawler.py' to test Crawler module
Run 'python test_cluster.py' to test Cluster module

3. Notice
Crawler may trigger the linkedin verification mechanism.To solve this problem, you can set your own account at parameters.py, 
and run 'python /LinkedinCrawler/server/crawler/verify.py' to simulate the verification process, before start the Crawler.

# How to run this app locally
1. Needed tools
As the crawler module needs the help of chrome browser, make sure they have installed in your environment
There has been a ChromeDriver provided in the '/Users/feifanzhang/LinkedinCrawler/server/static', 
if it doesn't work, please download the right one at:http://chromedriver.chromium.org/

2. Front-end
1) Make sure you have installed Node and npm
2) Go into the 'LinkedinCrawler/client/linkedin-cluster' folder
3) Run 'npm install' to install the needed library
4) Run 'npm start' to start the front-end, the front-end will running at http://localhost:3000/

3. Back-end
1) Make sure you have installed python and pip 
2) Install the python modules, you can use the requirements.txt in folder 'LinkedinCrawler/server'
   Here are the module list :
      matplotlib==2.2.4
      Flask==1.1.1
      parsel==1.5.1
      pandas==0.24.2
      Flask_RESTful==0.3.7
      selenium==3.141.0
      numpy==1.16.4
      scikit_learn==0.21.2
3) Go to the 'LinkedinCrawler/server', rum 'python server.py', the server will running at  http://localhost:5000/

# How to deploy this app on cloud
1) Get a cloud VM
2) Go into the 'LinkedinCrawler/client/linkedin-cluster' folder, run 'npm run build', 
   it will generate static files in build folder
3) Send front-end static files to cloud VM, use Nginx to serve them
4) Send server code to cloud VM, use python supervisor module to start as a service
5) Set Nginx to proxy front-end request to back-end service

# Demo
Check http://20.36.38.226/ to see the lively demo.
It provides demo data (100 user profile), you can also fetch your own data at Crawler page.


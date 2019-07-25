# LinkedinCrawler
LinkedinCrawler can automatically collect basic Linkedin profiles and perform cluster algorithm on them, contains:
   - Crawler module
   - Cluster module
   - Front-end based on react framework and ant design ui
   - Back-end restful service based on flask framework

# Demo
Check http://20.36.38.226/ to see the lively demo.
It provides demo data (100 user profile), you can also fetch your own data at Crawler page.

# How to test crawler module
Location: `/LinkedinCrawler/server/crawler`
As only for demo prupose, data will be saved at '/LinkedinCrawler/server/static/userinfo.csv', the old data will be cleaned before the new ones come in.

1. Set linkedin account and other parameters at 'parameters.py', default provide a test account
2. Need Chrome browser installed
3. Need chromedriver(http://chromedriver.chromium.org/), there is one at '/LinkedinCrawler/server/static', replace it if it 
   doesn't work
4. Run 'python LinkedinCrawler/server/test/test_crawler.py' to see how it works

*notice: Crawler may trigger the linkedin verification mechanism. To solve this problem, you can set your own account at        parameters.py, and run 'python /LinkedinCrawler/server/crawler/verify.py' to simulate the verification process, and restart the Crawler. If it still doesn't work, you need login the Linkedin account at browser, and pass the robotic test.

# How to test cluster module
Location: '/LinkedinCrawler/server/cluster'
'/LinkedinCrawler/server/static/userinfo_demo.csv' stores data used for cluster

1. Use k-means algorithm to cluster the data, there are two ways to choose features:
   - The number of job description, he number of connection
   - The text content of job description, use TF-IDF deal with it
2. Run 'python LinkedinCrawler/server/test/test_cluster.py' to see how it works


# How to run services locally
Front-end
1. Make sure you have installed Node and npm
2. Go into the 'LinkedinCrawler/client/linkedin-cluster' folder
3. Run 'npm install' to install the needed library
4. Run 'npm start' to start the front-end, the front-end will running at http://localhost:3000/

Back-end
1. Make sure you have installed python and pip 
2. Install the python modules listed at 'LinkedinCrawler/server/requirements.txt': matplotlib, Flask, parsel, pandas,     
   Flask_RESTful, selenium, numpy, scikit_learn
3. Run 'python LinkedinCrawler/server/server.py', the server will running at  http://localhost:5000/

# How to deploy services on cloud
1. Connect to cloud VM
2. Go into the 'LinkedinCrawler/client/linkedin-cluster' folder, run 'npm run build', 
   it will generate static files in build folder
3. Send front-end static files to cloud VM, use Nginx to serve them
4. Send server code to cloud VM, use python supervisor module to start as a service
5. Set Nginx to proxy front-end request to back-end service




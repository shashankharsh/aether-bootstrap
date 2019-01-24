#### Data Fetcher

This utility allows for Jobs to be scheduled and executed.

To Run the utility:
 - Make changes to the default values in the local `./.env` file
 - run `docker-compose up` in this folder
 - visit `http://localhost:{PORT}` with the port value from `.env`
 - login with credentials from `.env`

 Gotchas:
 - If you want persistence when you destroy the container, you need to mount `/datastore.db` from the container. 

Currently the only Job type available is a REST Proxy which takes the result of one REST call and sends data to another endpoint. All of this is highly configurable, and limited manipulation of data is possible between the calls. Pagination and other high value features are supported.

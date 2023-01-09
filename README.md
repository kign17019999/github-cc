# github-cc

Welcome to my Cloud Computing Project :)

To begin the new environment please do following,

1. Create all necessary AWS instances.
2. Obtain the names of all the instances and put them in the config.conf file.
3. Edit the information in config.conf as needed (especially the link to the GitHub repository, which will be where the workers pull the code from when running the program).
4. Don't forget to set the AWS credentials in order to use the boto3 service.
5. To run the code on the master instance, follow these steps:
    - Update and install necessary packages: "sudo yum update && sudo yum install -y python3-pip vim git && sudo pip3 install -y"
    - Install numpy and boto3: "sudo pip3 install numpy boto3"
    - Clone the GitHub repository: "git clone URL..."
    - Go to the folder named 'github-cc': "cd github-cc"
    - Run the main application script: "python3 application_main.py"

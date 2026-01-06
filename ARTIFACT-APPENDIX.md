# Artifact Appendix (Required for all badges)

Paper title: **Are we collaborative yet? A Usability Perspective on Mixnet Latency for Real-Time Applications**

Requested Badge(s):
  - [ ] **Available**
  - [x] **Functional**
  - [ ] **Reproduced**


## Description (Required for all badges)
This is the artifact for the PETs 2026 paper "Are we collaborative yet? A Usability Perspective on Mixnet Latency for Real Time Applications.".

The paper details study of how users respond to different levels of latency under conditions similar to Mixnet usage. Participants in the study completed a series of general knowledge questions in a webapp that was designed by the authors. This artifact consists of the code for this webapp, and code to produce the results and statistics reported in the paper.

The web app firstly presents the information sheet and consent form for the study. It then presents 6 rounds of 14 general knowledge questions which are to be answered by the participant. In between each question round there is a short form where participants provided feedback on their experience. 

A second "participant" is also simulated using javascript, this simulated participant also attempts to answer the general knowledge questions. The simulated user and the real participant view their own document state and updates between these states are delayed by a varying parameter. 

### Security/Privacy Issues and Ethical Concerns (Required for all badges)

There is negligible security risk running this artifact. The artifact hosts a web server on port 8080 and does not engage in any other network communications.

The study received ethical approval form the UCL Computer Science Ethics comittee. Participants were recruited using the prolific.com service. They were presented with an information sheet and a consent form. They were paid £1.70 for their participation.

## Basic Requirements (Required for Functional and Reproduced badges)

### Hardware Requirements (Required for Functional and Reproduced badges)

Can run on a laptop (No special hardware requirements)

### Software Requirements (Required for Functional and Reproduced badges)


The software runs in a docker container using Python 3.11 and nodejs. Only docker is required to run the artifact. I have tested the docker image on debian 13 using Docker version 20.10.24


The artifact uses python packages such as flask to host the web app and matplotlib, plotly etc to craft the figures. The nodejs section requires the automerge package. All dependencies as listed in the requirements.txt file and the package.json file.

The statistical and graphical results can be computed using the real study data which is provided.

### Estimated Time and Storage Consumption (Required for Functional and Reproduced badges)

Approximately 450MB is required to build and run the docker image.
Replace the following with estimated values for:

Building and running the docker image should take a negligible amount of time. 13 seconds on my laptop from 2017.

Testing the functionality of the webapp in the browser could take approximately 5-10 minutes. 

Generating the figures and running the statistical tests should take less than 10 minutes.
## Environment (Required for all badges)

### Accessibility (Required for all badges)

The artifact is hosted on github here: https://github.com/KillianDavitt/mixnet-user-study

### Set up the environment (Required for Functional and Reproduced badges)

```bash
git clone https://github.com/KillianDavitt/mixnet-user-study
cd mixnet-user-study
```


### Testing the Environment (Required for Functional and Reproduced badges)

Check if you have docker properly installed

```bash
docker version
```

This artifact has been tested with docker version 20.10.24

## Artifact Evaluation (Required for Functional and Reproduced badges)

### Main Results and Claims

#### Main Result 1: webui
The webui used for the user study should be able to be seen and examined running.


#### Main Result 2: Figures and statistics

All of the figures and statistics used in the paper should be reproduced.

### Experiments

#### Experiment 1: Testing the webui
- Should take <5 min compute time, and about 10 minutes of human time.
```bash
cd webapp
docker build -t mixnet-user-study .
```

After successfully building the docker image, you can run the image as follows:

```bash
docker run -p 8080:8080 mixnet-user-study
```

While this is running you should be able to access the webpage on port 8080 via the link provided by docker. Please use the Docker provided IP address and not 127.0.0.1.

You can now complete the user study as the study participants did. After completing the study, the results are saved in an sqlite3 database, `db.sqlite'. 

You can check the contents of the response table. The following command is provided as an example showing some of the fields:

```sql
select prolific_id,delay,review,rating,end_time-start_time,education from response;
```

This database is then used to generate figures and statistics in experiment 2 (The real database from our user study deployment is provided).

#### Experiment 2: Generating figures and statistics

- 5 human-minutes + 5 compute minutes

```bash
cd results
docker build . --tag 'mixnet-results'
docker run --rm -v $(pwd)/figures:/figures/ mixnet-results
```

Once the commands have been run, please observe the three png images produced in the figures/ directory. These 3 png images correspond to the following 3 figures in the paper:

figure 2: frustration.png
figure 4: strategy.png
figure 3: perceived_time_diff.png

## Limitations (Required for Functional and Reproduced badges)

The artifact fully reproduces the application used by participants in our study. 

The artifact also reproduces all analysis and figures used in the paper.


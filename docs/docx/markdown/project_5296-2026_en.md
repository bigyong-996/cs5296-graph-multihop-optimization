CS5296 Cloud Computing, Spring 2026

Project:
•  You will form groups of up to THREE.
•  You can also choose to do the project individually. We have the same expectation for
individual projects and follow the same assessment rules (expect for page limit of the
final report)

•  On a group or individual basis, you will choose and study a problem/

algorithm/technology/product/company which is closely related to cloud computing or
edge computing (e.g., a mobile app, a social networking website, a new programming
language, a new virtualization technology, task offloading, digital twins, Metaverse,
LLM, UAV, etc.),

•  Nature of the project:

•  There are three choices to do the project:
•  Research: You will study a technical problem, propose a new solution to this
problem, and conduct performance evaluation of the proposed solution. The
solution can be incremental based on existing solutions, but there has to be
something new here. The maximum mark for research projects is 25.

•  Technical: You will study a technical problem, and implement/evaluate existing

solutions. The maximum mark for technical projects is 22.

•  Business: You will study a business, a start-up, or the business aspect of

some technology. The maximum mark for business projects is 20.

•  Deliverables:

•  A project proposal (2 marks).
•  A final report (15 marks).
•  A piece of software artifact (4 marks)
•  A demo (4 marks)

•  Grouping:

•  Form groups by yourselves. Fill out the grouping information on Canvas only

after you finalize the membership

•  Go to Canvas->People->5296_groups tab, where empty groups have been
created. Add yourselves to an empty group or an existing one. At most 3
members in each group.

Proposal:
•  Objective:

•  To help you get an early start for your project, instead of doing it in the last

minute

•  Content:

•  The subject of your project
•  The nature of your project
•  A brief summary of the subject, including the link of its website, and what you

will do for the project

•  Name and student ID of each member of your group. For individual projects,

write down “Individual project” as the sub-title of the proposal

•

•  Format:

•  Maximum 2-page A4 size, PDF format, single column, single spaced, 12pt

Times New Roman

•  The file name should be: Group_ID_proposal.pdf, e.g., Group_2_proposal.pdf

•  Submission:

•  Deadline: Feb 6, 2026, 23:59pm HKT
•  Submit via Canvas->Assignments->Group projects->Proposal. Only pdf file

is allowed. No late submission is allowed.

Final Report:

The report summarizes your findings of the project. It should, in general, have the
following sections (similar to an academic paper):
•  Title and authorship: Include your group ID in the author information.
•  Abstract: A short summary of your project, less than 250 words.
•  Introduction: Introduce the subject of your project, present the context, set up and
motivate the importance of the problem, present your methodology (survey, app dev
on EC2, simulation in Matlab, etc.), and explain the major findings. Present a clear,
logical, and interesting story.

•  Main part of your report: The main part of your report can be organized in one or

multiple sections depending on your judgement. You should present the details of the
subject you study, your new solutions (if any), how your experiments/implementation
are done, what are the observations of your performance evaluation/experiments,
and explain these observations.

•  Conclusion: Conclude your project in 3–4 sentences.
•  References: Include any papers/websites/sources that you cite in your report. You

can organize the references in the IEEE format (see here: https://ieee-
dataport.org/sites/default/files/analysis/27/IEEE%20Citation%20Guidelines.pdf)
•  Artifact appendix: This describes steps on how to reproduce your project. Refer to

“Artifact evaluation” section below for more details. This part does NOT count towards
the page limit.

You are encouraged to use LaTeX to write your report. A short guide can be found here:
https://www.latex-tutorial.com/tutorials/. Reports written with Word are acceptable too.

Format:
•  A4 or US Letter size (for LaTeX), PDF format, single column, single spaced, 12pt

Times New Roman

•  The file name should be: GroupID_report.pdf.
•  Page limit: 9 pages for group projects, 8 pages for individual projects (including

references)

Grading scheme:
(13 marks) Content, e.g., breadth and depth, novelty of the proposed solution, difficulty
and amount of work in implementation/experiments/measurements, etc.
(2 marks) Writing, e.g., the use of English, the logical structure of the presentation, etc.
Don’t make use of  Chatgpt or other LLM software to generate your report!

Submission:
•  Deadline: April 24, 2026, 23:59pm HKT
•  Submit via Canvas->Assignments->Group projects->Report. Only pdf file is

allowed. No late submission is allowed.

Software Artifact

Artifact evaluation aims at promoting the reproducibility of experimental results. By
"artifact" we mean a digital object that was either created to be used as part of the study
or generated by the experiment itself. For example, artifacts can be software
systems/source code, scripts used to run experiments, input datasets, raw data
collected in the experiment, or scripts used to analyze results1. You are required to
formally describe all supporting material (code, data, models, workflows, results) using a
special Artifact Appendix in your report.

**NOTE**: Business projects do NOT have software artifacts (hence the lower
maximum marks)

Preparing your Artifact Appendix:

You need to prepare the Artifact Appendix describing software/hardware dependencies,
how to prepare and run experiments, and which results to expect at the end of the
evaluation. You also need to provide at least some scripts to build your workflow, all
inputs to run your workflow, and some expected outputs to validate results from your
paper. We strongly encourage you to check the the Artifact Appendix guide before
submitting artifacts for evaluation! You can find the examples of Artifact Appendices in
the following reproduced papers.

Submission and review of artifacts will take place on GitHub. You should host the
artifact (code source, dataset, etc.) in your own GitHub repository. Once the project
report is due we will create a fork of your repository to our GitHub repository to ensure
the code represents exactly what was described in the report. Your GitHub repository
should be open to public, not private. You should also use git regularly as a version
control system to collaborate for your group project. (Lab 7 will be about git and
GitHub.)

1 https://www.acm.org/publications/policies/artifact-review-badging

Also, you are encouraged (but not required) to make a self-contained docker image or
VM image on EC2 or a VirtualBox virtual machine, which ensures all dependencies
have been installed and that we can directly start using the software. We do not have a
strict limit but strongly suggest to limit the space to several GB and avoid including
unnecessary software packages to your VM images. Please follow the links below for
further information about creating and sharing your own EC2 AMI, Docker image, or
VirtualBox VM image.

Format:
•  Identical to the final report requirements.
•  At the very least, include the link to the Github repository of your project.
•  All the details that enable us to properly use the artifacts can appear in a special

Appendix of your report which ensures easy reviewing and reproducibility.

•  Page limit: Artifact Appendix has no page limit and no effect on the final page count of

the report.

Grading scheme:
(0.5 marks) Appendix is clear and complete to understand, install, and evaluate
artifacts.
(0.5 marks) The use of portable workflow frameworks to standardize, automate and
simplify the artifact evaluation process (e.g., container or VM images, python scripts to
automatically build the software according to the environment, etc.).
(2 marks) Artifacts are found to be consistent, complete, runnable, and include
appropriate evidence of verification and validation.
(1 mark) The repo should have a history of all the commits from different group
members spanning a period of time. Repos with only the last-minute commit will NOT
receive this mark.

Submission:
•  The artifact appendix is to be submitted together with the report as a single pdf file via

Canvas. See the submission instructions for the report outlined before.

**NOTE**: Business projects do NOT need to submit software artifacts (hence the lower
maximum marks)

Demo video

You are to record a video to demonstrate your project. Here are some important
guidelines:
1.  The demo should include

•  A very short introduction of your project
•  General explanation of your solution
•  For research/technical projects, a live demo of running your artifact (code,

measurements, etc.)

•  For business projects, methodology of your investigation
•  Results and 1-2 important findings

2.  Use speech to explain your idea
3.  You can also edit the video by adding caption.
4.  The video resolution should not be less than 640 * 480.
5.  The demo should last for no more than 10 minutes.
6.  The language used in the demo is English only.

Grading Scheme
1.  Content (1.5 marks):

•  Required components and your key idea should be included
•  Practical solutions and clear instructions to run the solution

2.  Quality (2.5 marks):

•  Key points and innovative ideas are highlighted and explained.
•  Instructions of running the program should be clear and easy to follow for the

audience to reproduce the results

•  The length of the video is respected; proper and effective use of caption and

other means of editing to improve the quality

Tips for making the demo video
1.  Tools

•  For Windows users, download CamStudio at https://camstudio.org/. CamStudio

is a great tool for recording the screen.

•  For Mac users, you could record the screen by pressing Command + Shift + 5

and edit the video using the pre-installed application called iMovie.

2.  Try to record the window you are working on instead of the entire screen, unless

3.

you have to work with multiple applications/windows.
Important explanations can be highlighted with both speech and caption on the
screen.

Submission:
•  Deadline: April 24, 2026, 23:59pm HKT
•  First, upload your demo to either YouTube or bilibili, make it visible to the public

(otherwise we cannot see and grade it). You can create an account and upload videos
for free for both sites.

•  Then, submit the link of your demo via Canvas->Assignments->Group

projects->Demo. Only web link is allowed. No late submission is allowed.

•  Uploading to other sites (such as Baidu Netdisk) will result in zero mark for the demo

right away.

•  Selected outstanding demo videos will be shared to the entire class so everyone can

learn and enjoy.

Sample projects from previous years:

Research:
•  Gene Set Enrichment Analysis (GSEA) with MapReduce
•  SQL queries over encrypted data in public clouds
•  Sentimental analysis of customer reviews
Technical:
•  Network performance of Docker
•  Running machine learning workloads in public clouds (using GPU instances)

(*Caution: GPU instances can be quite expensive)
•  Performance benchmarking of cloud service providers
•  Container based virtualization vs. hypervisor based virtualization
•  Spark vs. Hadoop
Business:
•  Study of “Doctor on Demand”
•  Study of Netflix, Spotify, DiDi, etc.



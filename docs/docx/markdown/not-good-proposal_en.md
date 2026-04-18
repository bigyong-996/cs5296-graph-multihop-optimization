Project Proposal: Performance benchmarking of AWS EC2 instance
Nature: Technical

Introduction
Nowadays, with the growth of people realize the convenience and low-price of cloud
computing, the daily usage of cloud server also increases rapidly. Among the different
cloud  service  providers, Amazon Web  Services  (AWS)  is  the  most  famous  one  and
supports most of the users. For AWS, Elastic Compute Cloud  EC2 instances are the
most popular service. Therefore, from  the users’ point of view, before purchases the
EC2  instances,  learning  the  performance  of  different  EC2  instances  under  different
environment    is  really  important.  Hence,  this  project  aims  to  offer  the  particular
performance evaluation of AWS EC2 instances to the users.
Statement of problem
From users’ point of view, it is really important to learn the performance of different
EC2 instances under different environment before they deploy the corresponding work,
in  order to  achieve benefit maximization. The evaluation  of EC2  instances could  be
classified  into  two  aspects,  performance  of  instance  property  and  performance  of
network. In terms of    the instance property performance, user could search the basic
performance from AWS official documents[1] or learn the benchmarks of different type
of  instances  from  Cloudlook[2]  whose  results  are  based  on  abundant  measurements.
Hence, this project aims to measure the performance about CPU, memory, and I/O of
different type of EC2 instances, in order to evaluate the accuracy of previous assessment.
For  network  performance,  a  research[3]  offers  a  hint,  different  workload  might  be
deployed in different time with instances in different region. Therefore, it is necessary
for users to learning network performance in these two dimensionalities which also will
be evaluated in this project.
Objectives
•  Evaluate  the  CPU  performance,  memory  performance  and  I/O  performance  of
different type of EC2 instances.
•  Evaluate  the  network  performance  about TCP  throughput  and  Round Trip Time
(RTT) of EC2 instances deployed in different regions, and explore the variation law.
•  Evaluate the network performance in different time and explore the variation law.
Scope
For the first objective, this project aims to evaluate the EC2 instances about types T2,
T3, M4, M5.
For the second objective, this project aims to evaluate the EC2 instances deployed in N.
Virginia, Oregon, Tokyo, Ireland and Sao Paulo.
For  the  third  objective,  this  project  aims  to  evaluate  the  EC2  instances  network
performance in different time range of everyday in about one month and compare the
performance between workdays and non-workdays.
References website.
[1] https://aws.amazon.com/cn/ec2/instance-types/
[2] http://www.cloudlook.com/amazon-ec2-instance-types
[3]  https://www.burstorm.com/price-performance-benchmark/1st-Continuous-Cloud-
Price-Performance-Benchmarking.pdf



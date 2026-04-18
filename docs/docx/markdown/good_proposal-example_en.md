Subject: Benchmarking shadowsocks proxy server over the different type of EC2 instance

Project Members:

Nature of the project: Technical

Project Summary:

Shadowsocks(SS) is a tool to proxy the network like VPN, it is widely used in mainland China
to cross the firewall. Shadowsocks is an open source tool and its performance is influenced by
the VPS capability. A common understanding is that the VPS with large bandwidth and
powerful hardware can proxy more packets than basic VPS. In our project, we will install
Shadowsocks onto different type of EC2 instances, and we will measure and benchmark the
proxy capability and performance.

We will study the security of Shadowsocks. Recent reports suggest that machine learning
algorithms may be used to identify Shadowsocks traffic in the network, this makes the denial-
of-service applications deployed on the firewall possible. We will discuss the security of
Shadowsocks and discuss about possible countermeasures.

Shadowsocks essentially break through the limitations of network firewalls by proxying packets.
Shadowsocks uses the chacha2.0 and AES encryption algorithms to protect the proxy packets so
that interception of traffic cannot be implemented. In addition, optimization of TCP forwarding
on the server side can significantly improve the throughput of the SS. We will deploy the TCP
acceleration application on the SS server and test the relationship between its performance and
server hardware.

We will perform cost analysis on Shadowsocks and discuss the appropriate user types for
different types of AWS instances. This will be useful for university students in mainland China,
since they can apply AWS student account and make full use of their credit.

The overall stress testing and the benchmarking plan will be discussed throughout the team
meeting. To make sure the different server location and type of server will be tested by pre-
designed scripts.



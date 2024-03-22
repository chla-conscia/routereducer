
# RouteReducer

## Description
RouteReducer is a tool designed to optimize and summarize lists of IP subnets, supporting both IPv4 and IPv6 addresses. It takes a list of subnets, sorts them, and uses the `aggregate6` command-line tool to efficiently combine contiguous and adjacent subnets into larger blocks where possible. The tool produces a detailed report in both CSV and Excel formats, listing each summarized subnet along with its contributing original subnets and a status comment.

## Structure
```
.
├── README.txt
├── ipv4
│   ├── routereducer_ipv4.py
│   └── subnets.txt
└── ipv6
    ├── routereducer_ipv6.py
    └── subnets.txt
```

## Requirements
- Python 3.x
- `pandas` and `xlsxwriter` libraries
- `aggregate6` command-line tool

## Installation

- ### Prerequisites
1. Ensure Python 3 and pip are installed on your system.

### Install Python Libraries
2. Install the required Python libraries with the following command:
```
pip install pandas xlsxwriter
```

### Install aggregate6
3. `aggregate6` can be installed differently depending on your operating system:

#### For general use or for systems not covered below:
```
pip3 install aggregate6
```
>(ensure pip is for Python 3)
- #### OpenBSD:
```
doas pkg_add aggregate6
```
- #### CentOS/RHEL/Rocky:
```
yum install epel-release
yum install aggregate6
```
- #### Fedora:
```
dnf install aggregate6
```
For more detailed instructions, see the `aggregate6` GitHub repository:
 [https://github.com/job/aggregate6](https://github.com/job/aggregate6)


## Usage
1. Place your list of subnets in the `subnets.txt` file located in the appropriate directory (`ipv4` or `ipv6`).
2. Run the corresponding Python script:
```
python routereducer_ipv4.py
# or
python routereducer_ipv6.py
```

## Subnets Example
IPv4 Subnets Example:
```
172.16.2.0/24
10.0.0.0/25
172.16.0.0/24
192.168.0.0/24
10.0.0.128/25
192.168.1.0/24
```

IPv6 Subnets Example:
```
2001:db8::/32
2001:db8:1::/64
fd00:abcd:12::/64
fd00:abcd:13::/64
2607:f8b0:4005::/48
2607:f8b0:4007::/48
```

## License
RouteReducer is released under the MIT License.

## Acknowledgements
RouteReducer uses `aggregate6` by Job Snijders, available at [https://github.com/job/aggregate6](https://github.com/job/aggregate6).

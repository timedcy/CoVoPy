#! /usr/bin/python2

import dpkt
import socket
import pygeoip
import optparse

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def retGeoStr(ip):
    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        country = rec['country_code3']
        if city != '':
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc
    except:
        return 'Unregistered'

def printPcap(pcap):
    st = set()
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            if not (src, dst) in st:
                print '[ + ] Src : %s(%s) --> Dst : %s(%s)' % \
                    (src, retGeoStr(src), dst, retGeoStr(dst))
                st.add((src, dst))
        except:
            pass

def main():
    parser = optparse.OptionParser('usage %prog -p <pcap file>')
    parser.add_option('-p', dest = 'pcapFile', type = 'string', help = 'specify pcap file')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print parser.usage
        exit(0)
    pcapFile = options.pcapFile
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)


if __name__ == '__main__':
    main()

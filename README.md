check_varnishbackends.py
=============

##Overview

This health check allows you to monitor the state of your backends for Nagios/Icinga.  

### Usage

<pre><code>
  -h, --help                   Show help message and exit
  -H HOST, --host=HOST         The ip varnishadm is listening on (Default: 127.0.0.1)
  -P PORT, --port=PORT         The port varnishadm is listening on (Default: 6082)
  -s SECRET, --secret=SECRET   The path to the secret file (Default: /etc/varnish/secret)
  -p PATH, --path=PATH         The path to the varnishadm binary (Default: /usr/bin/varnishadm
   Example: ./check_varnishbackends.py -H 127.0.0.1 -P 6082 -S /etc/varnish/secret -p /usr/bin/varnishadm
</pre></code>

## Frequently Asked Questions

### I am getting "No backends detected"
#### Ensure you have a .probe configured such as,
<pre><code>backend default {
  .host = "127.0.0.1";
  .port = "80";
  .probe = {
        .url = "/";
        .interval = 5s;
        .timeout = 5s;
        .window = 5;
        .threshold = 3;
  }
}
</pre></code>


## Change Log

## v1.1 - 2 July 2014
- Added notice regarding .probe
- Merged into own repo with active change log

## v1.0 - 19 April 2012
- Initial Release
- Updating Contact information


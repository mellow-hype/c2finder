# c2finder

*Mandatory disclaimer: I am not a master coder by any means, so this is a very simple script. Do not rely on this to be perfect. I am open to feedback or ideas for improvements, though :)*
“This package is free software; the copyright holder gives unlimited permission to copy and/or distribute
it, with or without modifications, as long as this notice is preserved. This package is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY, to the extent permitted by law; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.” 
I am not responsible for any kind of misuse of this code.
## Description
This script downloads the master C&C list from Bambanek Consulting (http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt), parses it, and searches through Bro logs for occurences of the C&C IPs. It saves the Bro entries that contained the C&C IPs to separate files for each IP and saves it's own output to a log file named in the format `c2finder_[date].log`.

## Usage Examples

```
./c2finder.py bro/logs/current/dns
./c2finder.py bro/logs/current/http
./c2finder.py bro/logs/current/files
```

## Modifying bro-cut fields
The script is preconfigured with some basic bro-cut selections. If you would like to search in different fields or get other fields in your logs, it's as easy as modifying the commands in the BROCUT dictionary at the beginning of the main section.

Retrieves all the symbols available on Yahoo Finance and stores them in a file for subsequent processing.
Currently just the ticker symbol is retrieved.  

_Takes a few hours to run._  It's brute force but works.

# Running the script
```
python yh_get_all_sym.py
```

If you get an error running the script, you *may* need to install python libraries.  
If so, use `pip install <library name>` .  The only ones I am using are logging and requests.

# Output
- Tickers are stored in a file with name yh_all_symbols.txt 
- Output file format is structured as a python set: { 'ticker1', 'ticker2' ... }  
- File is located in the same folder you launched python script from
- Output file size is about 16MB
- Console messages are shown while the script is executing
- Log file contains the console messages is stored in yh_get_all_sym.log

# Sample output

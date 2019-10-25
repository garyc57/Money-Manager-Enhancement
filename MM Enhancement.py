import sqlite3

##############
#
# Beginning of the main code
#
##############

conn = sqlite3.connect('B:\Money Manager EX\Crocketts.mmb')

c = conn.cursor()

cSelect = """SELECT AccountId, AccountName, AccountType FROM AccountList_V1 WHERE AccountType in ('Checking','Credit Card');"""
c.execute( cSelect )
accts = c.fetchall()
for tid, name, ctype in accts:
    print( f"{tid:{4}} {name:30} {ctype}")
print()
cSelect = """SELECT TransId
                  , ToAccountId
                  , TransCode
                  , TransAmount
                  , Notes
                  , TransDate
               FROM CheckingAccount_V1
              WHERE AccountId = 1
                AND TransDate > '2019-08'
                and TransCode = 'Transfer'
           ORDER BY TransDate DESC;"""
c.execute( cSelect )
checks = c.fetchall()
for tid, acct, code, amt, notes, tDate in checks:
    print( f"{tid:{4}} {tDate} {acct} {code:10} {amt:7.2f} {notes}")

c.close()
conn.close()

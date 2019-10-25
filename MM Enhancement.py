import sqlite3

def get_bal( dAsOf, nBegBal ):
    c.execute("""SELECT SUM( Withdrawal )
                   FROM Trans
                  WHERE Date <= :AsOf""", {'AsOf': dAsOf})
    nChecks = c.fetchone()[0]
    if nChecks is None:
        nChecks = 0

    c.execute("""SELECT SUM( Deposit )
                   FROM Trans
                  WHERE Date <= :AsOf""", {'AsOf': dAsOf})
    nDeps = c.fetchone()[0]
    if nDeps is None:
        nDeps = 0

    return nBegBal + nDeps - nChecks

def nice_print( cString, nNum ):
    cTemp = cString + ':'
    cTemp = cTemp.rjust(17)
    print( f"{cTemp} {nNum:{cFormat}}")
    
##############
#
# Beginning of the main code
#
##############
conn = sqlite3.connect('B:\Money Manager EX\Crocketts.mmb')
c = conn.cursor()
cFormat = '>9,.2f'

cSelect1 = """SELECT InitialBal
                FROM AccountList_V1
               WHERE AccountId = 1
           """
c.execute( cSelect1 )
nInit = c.fetchone()[0]
nice_print( 'Initial Balance', nInit)

cSelect3 = """SELECT SUM( TransAmount )
                FROM CheckingAccount_V1
               WHERE ( AccountId = 1 )
                 AND TransDate < '2017-01-01'
                 AND TransCode = 'Deposit';
           """
c.execute( cSelect3 )
nDeps = c.fetchone()[0]
nice_print( 'Deposits', nDeps)

cSelect4 = """SELECT SUM( TransAmount )
                FROM CheckingAccount_V1
               WHERE ( AccountId = 1 )
                 AND TransDate < '2017-01-01'
                 AND TransCode = 'Withdrawal';
           """
c.execute( cSelect4 )
nWiths = c.fetchone()[0]
nice_print( 'Withdrawals', nWiths)

cSelect5 = """SELECT SUM( TransAmount )
                FROM CheckingAccount_V1
               WHERE ( ToAccountId = 1 )
                 AND TransDate < '2017-01-01'
                 AND TransCode = 'Transfer';
           """
c.execute( cSelect5 )
nTrans = c.fetchone()[0]
nice_print( 'Transfers', nTrans)

nNewBal = nInit + nDeps - nWiths + nTrans
nice_print( 'Ending Balance', nNewBal)


c.close()
conn.close()

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

def run_query( cQuery ):
    c.execute( cQuery )
    return c.fetchone()[0]
    
##############
#
# Beginning of the main code
#
##############
conn = sqlite3.connect('B:\Money Manager EX\Crocketts.mmb')
c = conn.cursor()
cCutOff = '2017-01-01'
cFormat = '>9,.2f'

cSelect1 = """SELECT InitialBal
                FROM AccountList_V1
               WHERE AccountId = 1
           """
c.execute( cSelect1 )
nInit = c.fetchone()[0]
nice_print( 'Initial Balance', nInit)

cSelect = """SELECT SUM( TransAmount )
               FROM CheckingAccount_V1
              WHERE ( AccountId = 1 )
                AND TransDate < '""" + cCutOff + """'
                AND TransCode = 'Deposit';
          """
nDeps = run_query( cSelect )
nice_print( 'Deposits', nDeps)

cSelect = """SELECT SUM( TransAmount )
               FROM CheckingAccount_V1
              WHERE ( AccountId = 1 )
                AND TransDate < '""" + cCutOff + """'
                AND TransCode = 'Withdrawal';
          """
nWiths = run_query( cSelect )
nice_print( 'Withdrawals', nWiths)

cSelect5 = """SELECT SUM( TransAmount )
                FROM CheckingAccount_V1
               WHERE ( ToAccountId = 1 )
                 AND TransDate < '""" + cCutOff + """'
                 AND TransCode = 'Transfer';
           """
c.execute( cSelect5 )
nTransIn = c.fetchone()[0]
nice_print( 'Transfers In', nTransIn)


cSelect5 = """SELECT SUM( TransAmount )
                FROM CheckingAccount_V1
               WHERE ( AccountId = 1 )
                 AND TransDate < '""" + cCutOff + """'
                 AND TransCode = 'Transfer';
           """
c.execute( cSelect5 )
nTransOut = c.fetchone()[0]
nice_print( 'Transfers Out', nTransOut)

nNewBal = nInit + nDeps - nWiths + nTransIn - nTransOut
nice_print( 'Ending Balance', nNewBal)

cSelect = """SELECT COUNT(1)
               FROM CheckingAccount_V1
              WHERE ( AccountId = 1 )
                AND TransDate < '""" + cCutOff + """'
                AND Status <> 'R';
          """

c.execute( cSelect )
nOut = c.fetchone()[0]
cMsg = 'No outstanding transactions'
if nOut != 0:
    cMsg = 'There are ' + str( nOut ) + ' outstanding transactions'
    print( cMsg )


c.close()
conn.close()

import datetime as dt
import logging

import azure.functions as func
import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
import numpy as np

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pretty_html_table import build_table

def main():#(mytimer: func.TimerRequest) -> None:
    ticker_list = ['PLTR','SPY','QQQ','TQQQ','SQQQ','A','AAL','AAP','AAPL','ABBV','ABC','ABT','ACN','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ','AJG','AKAM','ALB','ALGN','ALK','ALL','ALLE',
                   'AMAT','AMCR','AMD','AME','AMGN','AMP','AMT','AMZN','ANET','ANSS','ANTM','AON','AOS','APA','APD','APH','APTV','ARE','ATO','ATVI','AVB','AVGO','AVY','AWK','AXP',
                   'AZO','BA','BAC','BAX','BBWI','BBY','BDX','BEN','BF.B','BIIB','BIO','BK','BKNG','BKR','BLK','BLL','BMY','BR','BRK.B','BRO','BSX','BWA','BXP','C','CAG','CAH','CARR','CAT'
                   'B','COE','CBRE','CCI','CCL','CDAY','CDNS','CDW','CE','CERN','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX','CMA','CMCSA','CME','CMG','CMI','CMS','CNC','CNP','COF','COO',
                   'COP','COST','CPB','CPRT','CRL','CRM','CSCO','CSX','CTAS','CTLT','CTRA','CTSH','CTVA','CTXS','CVS','CVX','CZR','D','DAL','DD','DE','DFS','DG','DGX','DHI','DHR','DIS',
                   'DISCA','DISCK','DISH','DLR','DLTR','DOV','DOW','DPZ','DRE','DRI','DTE','DUK','DVA','DVN','DXC','DXCM','EA','EBAY','ECL','ED','EFX','EIX','EL','EMN','EMR','ENPH','EOG','EQIX',
                   'EQR','ES','ESS','ETN','ETR','ETSY','EVRG','EW','EXC','EXPD','EXPE','EXR','F','FANG','FAST','FB','FBHS','FCX','FDX','FE','FFIV','FIS','FISV','FITB','FLT','FMC','FOX','FOXA',
                   'FRC','FRT','FTNT','FTV','GD','GE','GILD','GIS','GL','GLW','GM','GNRC','GOOG','GOOGL','GPC','GPN','GPS','GRMN','GS','GWW','HAL','HAS','HBAN','HBI','HCA','HD','HES','HIG',
                   'HII','LT','HOLX','HON','HPE','HPQ','HRL','HSIC','HST','HSY','HUM','HWM','IBM','ICE','IDXX','IEX','IFF','ILMN','INCY','INFO','INTC','INTU','IP','IPG','IPGP','IQV','IR',
                   'IRM','ISRG','IT','ITW','IVZ','J','JBHT','JCI','JKHY','JNJ','JNPR','JPM','K','KEY','KEYS','KHC','KIM','KLAC','KMB','KMI','KMX','KO','KR','KSU','L','LDOS','LEG','LEN','LH',
                   'LHX','LIN','LKQ','LLY','LMT','LNC','LNT','LOW','LRCX','LUMN','LUV','LVS','LW','LYB','LYV','MA','MAA','MAR','MAS','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','MGM','MHK',
                   'MKC','KTX','MLM','MMC','MMM','MNST','MO','MOS','MPC','MPWR','MRK','MRNA','MRO','MS','MSCI','MSFT','MSI','MTB','MTCH','MTD','MU','NCLH','NDAQ','NEE','NEM','NFLX','NI','NKE',
                   'NLOK','NLSN','NOC','NOW','NRG','NSC','NTAP','NTRS','NUE','NVDA','NVR','NWL','NWS','NWSA','NXPI','O','ODFL','OGN','OKE','OMC','ORCL','ORLY','OTIS','OXY','PAYC','PAYX','PBCT',
                   'PCAR','PEAK','PEG','PENN','PEP','PFE','PFG','PG','PGR','PH','PHM','PKG','PKI','PLD','PM','PNC','PNR','PNW','POOL','PPG','PPL','PRU','PSA','PSX','PTC','PVH','PWR','PXD','PYPL',
                   'QCOM','QRVO','RCL','RE','REG','REGN','RF','RHI','RJF','RL','RMD','ROK','ROL','ROP','ROST','RSG','RTX','SBAC','SBUX','SCHW','SEE','SHW','SIVB','SJM','SLB','SNA','SNPS','SO',
                   'SPG','SPGI','SRE','STE','STT','STX','STZ','SWK','SWKS','SYF','SYK','SYY','T','TAP','TDG','TDY','TECH','TEL','TER','TFC','TFX','TGT','TJX','TMO','TMUS','TPR','TRMB','TROW','TRV','TSCO','TSLA','TSN','TT','TTWO',
                   'TXN','TXT','TYL','UA','UAA','UAL','UDR','UHS','ULTA','UNH','UNP','UPS','URI','USB','V','VFC','VIAC','VLO','VMC','VNO','VRSK','VRSN','VRTX','VTR','VTRS','VZ','WAB','WAT','WBA','WDC','WEC','WELL','WFC','WHR','WLTW','WM','WMB','WMT','WRB','WRK','WST','WU','WY','WYNN','XEL','XLNX','XOM','XRAY','XYL','YUM','ZBH','ZBRA','ZION','ZTS',
                   'AADI', 'AAN', 'AAON', 'AAT', 'ABCB', 'ABCL', 'ABG', 'ABM', 'ABR', 'ABSI', 'ABUS', 'AC', 'ACA', 'ACAD', 'ACCD', 'ACCO', 'ACEL', 'ACET', 'ACHR', 'ACIW', 'ACLS', 'ACLX', 'ACMR', 'ACNB', 'ACRE', 'ACRS', 'ACRV', 'ACT', 'ACVA', 'ADC', 'ADEA', 'ADMA', 'ADNT', 'ADPT', 'ADTH', 'ADTN', 'ADUS', 'ADV', 'AEIS', 'AEL', 'AEO', 'AEVA', 'AFCG', 'AFMD', 'AGEN', 'AGIO', 'AGM', 'AGTI', 'AGX', 'AGYS', 'AHCO', 'AHH', 'AHT', 'AI', 'AIN', 'AIP', 'AIR', 'AIRS', 'AIT', 'AIV', 'AJRD', 'AKA', 'AKR', 'AKRO', 'AKTS', 'AKYA', 'ALCO', 'ALE', 'ALEC', 'ALEX', 'ALG', 'ALGT', 'ALHC', 'ALIT', 'ALKS', 'ALKT', 'ALLO', 'ALPN', 'ALRM', 'ALRS', 'ALTG', 'ALTO', 'ALTR', 'ALVR', 'ALX', 'ALXO', 'AMAL', 'AMBA', 'AMBC', 'AMCX', 'AMEH', 'AMK', 'AMKR', 'AMLX', 'AMN', 'AMNB', 'AMOT', 'AMPH', 'AMPL', 'AMPS', 'AMPY', 'AMR', 'AMRC', 'AMRK', 'AMRS', 'AMRX', 'AMSF', 'AMSWA', 'AMTB', 'AMTX', 'AMWD', 'AMWL', 'ANAB', 'ANDE', 'ANF', 'ANGO', 'ANIK', 'ANIP', 'ANTX', 'AOMR', 'AORT', 'AOSL', 'APAM', 'APEI', 'APG', 'APLD', 'APLE', 'APLS', 'APOG', 'APPF', 'APPH', 'APPN', 'APPS', 'ARCB', 'ARCH', 'ARCT', 'AREN', 'ARGO', 'ARI', 'ARIS', 'ARKO', 'ARL', 'ARLO', 'ARNC', 'AROC', 'AROW', 'ARQT', 'ARR', 'ARRY', 'ARTNA', 'ARVN', 'ARWR', 'ASAN', 'ASB', 'ASC', 'ASGN', 'ASIX', 'ASLE', 'ASO', 'ASPN', 'ASTE', 'ASTR', 'ATEC', 'ATEN', 'ATER', 'ATEX', 'ATGE', 'ATHA', 'ATI', 'ATIP', 'ATKR', 'ATLC', 'ATNI', 'ATOM', 'ATRA', 'ATRC', 'ATRI', 'ATRO', 'ATSG', 'AUB', 'AUPH', 'AURA', 'AVA', 'AVAH', 'AVAV', 'AVD', 'AVDX', 'AVID', 'AVIR', 'AVNS', 'AVNT', 'AVNW', 'AVO', 'AVPT', 'AVTA', 'AVTE', 'AVXL', 'AWR', 'AX', 'BTAI', 'BTU', 'BUSE', 'BV', 'BVH', 'BVS', 'BW', 'BWB', 'BWFG', 'BXC', 'BXMT', 'BY', 'BYND', 'BZH', 'CAC', 'CADE', 'CAKE', 'CAL', 'CALM', 'CALX', 'CANO', 'CARA', 'CARE', 'CARG', 'CARS', 'CASA', 'CASH', 'CASS', 'CATC', 'CATO', 'CATY', 'CBAN', 'CBL', 'CBNK', 'CBRL', 'CBT', 'CBU', 'CBZ', 'CCB', 'CCBG', 'CCCC', 'CCF', 'CCNE', 'CCO', 'CCOI', 'CCRN', 'CCS', 'CCSI', 'CDE', 'CDLX', 'CDMO', 'CDNA', 'CDRE', 'CDXS', 'CEIX', 'CELH', 'CELL', 'CELU', 'CENN', 'CENT', 'CENTA', 'CENX', 'CERE', 'CERS', 'CEVA', 'CFB', 'CFFN', 'CGEM', 'CHCO', 'CHCT', 'CHEF', 'CHGG', 'CHRD', 'CHRS', 'CHS', 'CHUY', 'CHX', 'CIFR', 'CIM', 'CIO', 'CIR', 'CISO', 'CIVB', 'CIVI', 'CIX', 'CLAR', 'CLBK', 'CLDT', 'CLDX', 'CLFD', 'CLNE', 'CLOV', 'CLPR', 'CLSK', 'CLW', 'CMAX', 'CMBM', 'CMC', 'CMCO', 'CMLS', 'CMP', 'CMPO', 'CMPR', 'CMRE', 'CMRX', 'CMTG', 'CMTL', 'CNDT', 'CNK', 'CNMD', 'CNNE', 'CNO', 'CNOB', 'CNS', 'CNSL', 'CNTY', 'CNX', 'CNXN', 'COCO', 'CODI', 'COGT', 'COHU', 'COKE', 'COLL', 'COMM', 'COMP', 'CONN', 'COOK', 'COOP', 'CORT', 'COUR', 'CPE', 'CPF', 'CPK', 'CPRX', 'CPSI', 'CPSS', 'CPTN', 'CRAI', 'CRBU', 'CRC', 'CRDA', 'CRDO', 'CRGE', 'CRGY', 'CRK', 'CRMT', 'CRNC', 'CRNX', 'CROX', 'CRS', 'CRSR', 'CRVL', 'CSGS', 'CSR', 'CSTE', 'CSTL', 'CSTM', 'CSTR', 'CSV', 'CSWI', 'CTBI', 'CTIC', 'CTKB', 'CTLP', 'CTO', 'CTOS', 'CTRE', 'CTRN', 'CTS', 'CTV', 'CUBI', 'CURO', 'CURV', 'CUTR', 'CVBF', 'CVCO', 'CVGW', 'CVI', 'CVLG', 'CVLT', 'CVT', 'CWEN', 'CWENA', 'CWH', 'CWK', 'CWST', 'CWT', 'CXW', 'CYH', 'CYRX', 'CYTK', 'CZNC', 'DAN', 'DAWN', 'DBI', 'DBRG', 'DC', 'DCGO', 'DCO', 'DCOM', 'DCPH', 'DDD', 'DDS', 'DEA', 'DEN', 'DENN', 'DFH', 'DFIN', 'DGICA', 'DGII', 'DHC', 'DHIL', 'DHT', 'DHX', 'DIBS', 'DICE', 'DIN', 'DIOD', 'DJCO', 'DK', 'DLTH', 'DLX', 'DM', 'DMRC', 'DNLI', 'DNMR', 'DNOW', 'DNUT', 'DO', 'DOC', 'DOCN', 'DOMA', 'DOMO', 'DOOR', 'DORM', 'DOUG', 'DRH', 'DRQ', 'DSEY', 'DSGN', 'DSGR', 'DSKE', 'DSP', 'DTC', 'DUOL', 'DVAX', 'DX', 'DXLG', 'DXPE', 'DY', 'DYN', 'DZSI', 'EAF', 'EAT', 'EB', 'EBC', 'EBF', 'EBIX', 'EBS', 'EBTC', 'ECPG', 'ECVT', 'EDIT', 'EE', 'EFC', 'EFSC', 'EGAN', 'EGBN', 'EGHT', 'EGIO', 'EGLE', 'EGRX', 'EGY', 'EHTH', 'EIG', 'EIGR', 'ELF', 'ELME', 'EMBC', 'EME', 'ENFN', 'ENOB', 'ENR', 'ENS', 'ENSG', 'ENTA', 'ENV', 'ENVA', 'ENVX', 'EOLS', 'EP', 'EPAC', 'EPC', 'EPRT', 'EQBK', 'EQC', 'EQRX', 'ERAS', 'ERII', 'ESE', 'ESGR', 'ESMT', 'ESNT', 'ESPR', 'ESQ', 'ESRT', 'ESTE', 'ETD', 'ETRN', 'ETWO', 'EVBG', 'EVC', 'EVCM', 'EVER', 'EVGO', 'EVH', 'EVLV', 'EVRI', 'EVTC', 'EWCZ', 'EWTX', 'EXLS', 'EXPI', 'EXPO', 'EXPR', 'EXTR', 'EYE', 'EYPT', 'EZPW', 'FA', 'FARO', 'FATE', 'FBIZ', 'FBK', 'FBMS', 'FBNC', 'FBP', 'FBRT', 'FC', 'FCBC', 'FCEL', 'FCF', 'FCFS', 'FCPT', 'FCUV', 'FDMT', 'FDP', 'FEAM', 'FELE', 'FF', 'FFBC', 'FFIC', 'FFIE', 'FFIN', 'FFWM', 'FGBI', 'FGEN', 'FHI', 'FHTX', 'FIBK', 'FIGS', 'FISI', 'FIX', 'FIZZ', 'FL', 'FLGT', 'FLIC', 'FLL', 'FLNC', 'FLNG', 'FLR', 'FLWS', 'FLYW', 'FMAO', 'FMBH', 'FMNB', 'FN', 'FNA', 'FNKO', 'FNLC', 'FOA', 'FOCS', 'FOLD', 'FOR', 'FORG', 'FORM', 'FORR', 'FOSL', 'FOXF', 'FPI', 'FRBA', 'FRBK', 'FREE', 'FRG', 'FRME', 'FRO', 'FRPH', 'FRST', 'FSBC', 'FSLY', 'FSP', 'FSR', 'FSS', 'FTCI', 'FTDR', 'FUBO', 'FUL', 'FULC', 'FULT', 'FVCB', 'FWRD', 'FWRG', 'FXLV', 'GABC', 'GAMB', 'GATX', 'GBCI', 'GBIO', 'GBX', 'GCBC', 'GCI', 'GCMG', 'GCO', 'GDEN', 'GDOT', 'GDYN', 'GEF', 'GEFB', 'GEO', 'GERN', 'GES', 'GEVO', 'GFF', 'GHC', 'GIC', 'GIII', 'GKOS', 'GLDD', 'GLNG', 'GLRE', 'GLT', 'GLUE', 'GMRE', 'GMS', 'GNK', 'GNL', 'GNTY', 'GNW', 'GOEV', 'GOGL', 'GOGO', 'GOLF', 'GOOD', 'GOSS', 'GPI', 'GPMT', 'GPOR', 'GPRE', 'GPRO', 'GRBK', 'GRC', 'GREE', 'GRNA', 'GRPN', 'GRWG', 'GSAT', 'GSBC', 'GSHD', 'GT', 'GTLS', 'GTN', 'GTY', 'GVA', 'GWH', 'GWRS', 'HA', 'HAE', 'HAFC', 'HAIN', 'HALO', 'HASI', 'HAYN', 'HBCP', 'HBNC', 'HBT', 'HCAT', 'HCC', 'HCCI', 'HCI', 'HCKT', 'HCSG', 'HDSN', 'HEAR', 'HEES', 'HELE', 'HFFG', 'HFWA', 'HGV', 'HI', 'HIBB', 'HIFS', 'HIMS', 'HIPO', 'HL', 'HLF', 'HLGN', 'HLI', 'HLIO', 'HLIT', 'HLLY', 'HLMN', 'HLNE', 'HLTH', 'HLVX', 'HLX', 'HMN', 'HMPT', 'HMST', 'HNI', 'HNST', 'HOMB', 'HONE', 'HOPE', 'HOUS', 'HOV', 'HP', 'HPK', 'HQY', 'HRI', 'HRMY', 'HRT', 'HRTX', 'HSC', 'HSII', 'HSTM', 'HT', 'HTBI', 'HTBK', 'HTH', 'HTLD', 'HTLF', 'HUBG', 'HUMA', 'HURN', 'HVT', 'HWC', 'HWKN', 'HY', 'HYFM', 'HYLN', 'HYMC', 'HYZN', 'HZO', 'IAS', 'IBCP', 'IBEX', 'IBOC', 'IBP', 'IBRX', 'IBTX', 'ICFI', 'ICHR', 'ICPT', 'ICVX', 'IDCC', 'IDT', 'IDYA', 'IE', 'IESC', 'IGMS', 'IGT', 'IHRT', 'III', 'IIIN', 'IIIV', 'IIPR', 'ILPT', 'IMAX', 'IMGN', 'IMKTA', 'IMVT', 'IMXI', 'INBK', 'INBX', 'INDB', 'INDI', 'INDT', 'INFN', 'INGN', 'INN', 'INNV', 'INO', 'INSE', 'INSG', 'INSM', 'INSP', 'INST', 'INSW', 'INT', 'INTA', 'INVA', 'INVE', 'IONQ', 'IOSP', 'IOVA', 'IPAR', 'IPI', 'IPSC', 'IRBT', 'IRDM', 'IRMD', 'IRNT', 'IRT', 'IRTC', 'IRWD', 'ISEE', 'ISPO', 'ITCI', 'ITGR', 'ITIC', 'ITOS', 'ITRI', 'IVR', 'IVT', 'IVVD', 'JACK', 'JANX', 'JBI', 'JBSS', 'JBT', 'JELD', 'JJSF', 'JMSB', 'JOAN', 'JOBY', 'JOE', 'JOUT', 'JRVR', 'JXN', 'JYNT', 'KAI', 'KALU', 'KALV', 'KAMN', 'KAR', 'KBH', 'KDNY', 'KE', 'KELYA', 'KFRC', 'KFY', 'KIDS', 'KLIC', 'KLR', 'KMT', 'KN', 'KNSA', 'KNSL', 'KNTE', 'KNTK', 'KOD', 'KODK', 'KOP', 'KORE', 'KOS', 'KPTI', 'KREF', 'KRG', 'KRNY', 'KRO', 'KRON', 'KROS', 'KRT', 'KRTX', 'KRUS', 'KRYS', 'KTB', 'KTOS', 'KURA', 'KW', 'KWR', 'KYMR', 'KZR', 'LADR', 'LANC', 'LAND', 'LASR', 'LAUR', 'LAW', 'LAZR', 'LBAI', 'LBC', 'LBRT', 'LC', 'LCII', 'LCUT', 'LE', 'LEGH', 'LEU', 'LFCR', 'LFST', 'LGFA', 'LGFB', 'LGIH', 'LGND', 'LICY', 'LIDR', 'LILA', 'LILAK', 'LIND', 'LIVN', 'LKFN', 'LL', 'LLAP', 'LMAT', 'LMND', 'LNN', 'LNTH', 'LNW', 'LOB', 'LOCL', 'LOCO', 'LOVE', 'LPG', 'LPRO', 'LPSN', 'LQDA', 'LQDT', 'LRN', 'LSEA', 'LTC', 'LTCH', 'LTH', 'LTHM', 'LUNG', 'LVLU', 'LVOX', 'LWLG', 'LXFR', 'LXP', 'LXRX', 'LXU', 'LYEL', 'LZ', 'LZB', 'MAC', 'MAPS', 'MARA', 'MASS', 'MATV', 'MATW', 'MATX', 'MAX', 'MBI', 'MBIN', 'MBUU', 'MBWM', 'MC', 'MCB', 'MCBC', 'MCBS', 'MCFT', 'MCRB', 'MCRI', 'MCS', 'MCY', 'MD', 'MDC', 'MDGL', 'MDRX', 'MDXG', 'ME', 'MED', 'MEDP', 'MEG', 'MEI', 'METC', 'MFA', 'MGEE', 'MGNI', 'MGNX', 'MGPI', 'MGRC', 'MGTX', 'MGY', 'MHO', 'MIR', 'MIRM', 'MITK', 'MKFG', 'MKTW', 'ML', 'MLAB', 'MLI', 'MLKN', 'MLNK', 'MLR', 'MLYS', 'MMI', 'MMS', 'MMSI', 'MNKD', 'MNRO', 'MNTK', 'MNTS', 'MOD', 'MODG', 'MODN', 'MODV', 'MOFG', 'MOGA', 'MORF', 'MOV', 'MPAA', 'MPB', 'MPLN', 'MPX', 'MQ', 'MRC', 'MRSN', 'MRTN', 'MSBI', 'MSEX', 'MSGE', 'MSTR', 'MTDR', 'MTH', 'MTRN', 'MTSI', 'MTTR', 'MTW', 'MTX', 'MULN', 'MUR', 'MUSA', 'MVBF', 'MVIS', 'MVST', 'MWA', 'MXCT', 'MXL', 'MYE', 'MYFW', 'MYGN', 'MYPS', 'MYRG', 'NABL', 'NAPA', 'NARI', 'NAT', 'NATR', 'NAUT', 'NAVI', 'NBHC', 'NBN', 'NBR', 'NBTB', 'NC', 'NDLS', 'NE', 'NEO', 'NEOG', 'NETI', 'NEX', 'NEXT', 'NFBK', 'NG', 'NGM', 'NGMS', 'NGVC', 'NGVT', 'NHC', 'NHI', 'NIC', 'NJR', 'NKLA', 'NKTR', 'NKTX', 'NL', 'NMIH', 'NMRK', 'NN', 'NNI', 'NNOX', 'NODK', 'NOG', 'NOTV', 'NOVA', 'NOVT', 'NPK', 'NPO', 'NR', 'NRC', 'NRDS', 'NRDY', 'NREF', 'NRGV', 'NRIX', 'NSIT', 'NSP', 'NSSC', 'NSTG', 'NTB', 'NTCT', 'NTGR', 'NTLA', 'NTST', 'NUS', 'NUTX', 'NUVA', 'NUVB', 'NUVL', 'NVEE', 'NVRO', 'NVTA', 'NWBI', 'NWE', 'NWLI', 'NWN', 'NWPX', 'NX', 'NXGN', 'NXRT', 'NXT', 'NYMT', 'OABI', 'OB', 'OBK', 'OCFC', 'OCGN', 'OCTO', 'OCUL', 'ODP', 'OEC', 'OFC', 'OFG', 'OFIX', 'OFLX', 'OGS', 'OI', 'OII', 'OIS', 'OLO', 'OLP', 'OM', 'OMCL', 'OMI', 'OMIC', 'ONB', 'ONDS', 'ONEW', 'ONL', 'ONTF', 'ONTO', 'OOMA', 'OPAD', 'OPCH', 'OPFI', 'OPI', 'OPK', 'OPRT', 'OPRX', 'OPY', 'ORA', 'ORC', 'ORGN', 'ORGO', 'ORRF', 'OSBC', 'OSCR', 'OSIS', 'OSPN', 'OSTK', 'OSUR', 'OSW', 'OTLK', 'OTTR', 'OUST', 'OUT', 'OXM', 'PACB', 'PACK', 'PAHC', 'PAR', 'PARR', 'PATK', 'PAYO', 'PBF', 'PBFS', 'PBH', 'PBI', 'PCB', 'PCH', 'PCRX', 'PCT', 'PCVX', 'PCYO', 'PD', 'PDCO', 'PDFS', 'PDLI', 'PDM', 'PEB', 'PEBO', 'PECO', 'PEPG', 'PETQ', 'PETS', 'PFBC', 'PFC', 'PFHC', 'PFIS', 'PFS', 'PFSI', 'PFSW', 'PGC', 'PGEN', 'PGNY', 'PGRE', 'PGTI', 'PHAT', 'PHR', 'PI', 'PIII', 'PIPR', 'PJT', 'PKBK', 'PKE', 'PL', 'PLAB', 'PLAY', 'PLBY', 'PLCE', 'PLL', 'PLM', 'PLMR', 'PLOW', 'PLPC', 'PLUS', 'PLXS', 'PLYM', 'PMT', 'PMVP', 'PNM', 'PNT', 'PNTG', 'POR', 'POWI', 'POWL', 'POWW', 'PPBI', 'PR', 'PRA', 'PRAA', 'PRAX', 'PRCH', 'PRCT', 'PRDO', 'PRDS', 'PRFT', 'PRG', 'PRGS', 'PRIM', 'PRK', 'PRLB', 'PRM', 'PRME', 'PRMW', 'PRO', 'PRPL', 'PRTA', 'PRTH', 'PRTS', 'PRVA', 'PSFE', 'PSMT', 'PSN', 'PSTL', 'PTCT', 'PTEN', 'PTGX', 'PTLO', 'PTRA', 'PTSI', 'PTVE', 'PUBM', 'PUMP', 'PVBC', 'PWP', 'PWSC', 'PZZA', 'QCRH', 'QLYS', 'QNST', 'QRTEA', 'QSI', 'QTRX', 'QTWO', 'QUAD', 'QUOT', 'RAD', 'RADI', 'RAMP', 'RAPT', 'RBB', 'RBBN', 'RBC', 'RBCAA', 'RBOT', 'RC', 'RCKT', 'RCKY', 'RCM', 'RCUS', 'RDFN', 'RDN', 'RDNT', 'RDVT', 'RDW', 'REAL', 'REFI', 'REI', 'RELY', 'RENT', 'REPL', 'REPX', 'RES', 'RETA', 'REVG', 'REX', 'REZI', 'RGNX', 'RGP', 'RGR', 'RGTI', 'RHP', 'RICK', 'RIDE', 'RIGL', 'RILY', 'RIOT', 'RKLB', 'RLAY', 'RLGT', 'RLI', 'RLJ', 'RLMD', 'RLYB', 'RM', 'RMAX', 'RMBL', 'RMBS', 'RMNI', 'RMR', 'RNA', 'RNST', 'ROAD', 'ROCC', 'ROCK', 'ROG', 'ROIC', 'ROOT', 'ROVR', 'RPAY', 'RPD', 'RPT', 'RRBI', 'RRR', 'RSI', 'RSVR', 'RTL', 'RUSHA', 'RUSHB', 'RVLV', 'RVMD', 'RVNC', 'RWT', 'RXDX', 'RXRX', 'RXST', 'RXT', 'RYAM', 'RYI', 'SABR', 'SAFE', 'SAFT', 'SAGE', 'SAH', 'SAIA', 'SAMG', 'SANA', 'SANM', 'SASR', 'SATS', 'SAVA', 'SAVE', 'SB', 'SBCF', 'SBGI', 'SBH', 'SBOW', 'SBRA', 'SBSI', 'SBT', 'SCHL', 'SCHN', 'SCL', 'SCS', 'SCSC', 'SCU', 'SCVL', 'SCWX', 'SD', 'SDGR', 'SEAS', 'SEAT', 'SEER', 'SEM', 'SENEA', 'SENS', 'SFBS', 'SFIX', 'SFL', 'SFM', 'SFNC', 'SFST', 'SG', 'SGC', 'SGH', 'SGHT', 'SGMO', 'SGRY', 'SHAK', 'SHBI', 'SHCR', 'SHEN', 'SHLS', 'SHO', 'SHOO', 'SHYF', 'SIBN', 'SIG', 'SIGA', 'SIGI', 'SILK', 'SITC', 'SITM', 'SJW', 'SKIL', 'SKIN', 'SKLZ', 'SKT', 'SKWD', 'SKY', 'SKYT', 'SKYW', 'SLAB', 'SLCA', 'SLDP', 'SLGC', 'SLP', 'SLQT', 'SLVM', 'SM', 'SMBC', 'SMBK', 'SMCI', 'SMMF', 'SMP', 'SMPL', 'SMR', 'SMRT', 'SMTC', 'SNBR', 'SNCE', 'SNCY', 'SNDX', 'SNEX', 'SNPO', 'SOI', 'SOND', 'SONO', 'SOVO', 'SP', 'SPCE', 'SPFI', 'SPHR', 'SPIR', 'SPNS', 'SPNT', 'SPSC', 'SPT', 'SPTN', 'SPWH', 'SPWR', 'SPXC', 'SQSP', 'SR', 'SRCE', 'SRDX', 'SRI', 'SSB', 'SSD', 'SSP', 'SSTI', 'SSTK', 'STAA', 'STAG', 'STBA', 'STC', 'STEL', 'STEM', 'STEP', 'STER', 'STGW', 'STHO', 'STKL', 'STKS', 'STNE', 'STNG', 'STOK', 'STR', 'STRA', 'STRC', 'STRL', 'STRO', 'STRS', 'SUM', 'SUNL', 'SUPN', 'SVC', 'SWAV', 'SWBI', 'SWI', 'SWIM', 'SWKH', 'SWTX', 'SWX', 'SXC', 'SXI', 'SXT', 'SYBT', 'SYNA', 'TALO', 'TALS', 'TARS', 'TBBK', 'TBI', 'TBPH', 'TCBI', 'TCBK', 'TCBX', 'TCI', 'TCMD', 'TCS', 'TCX', 'TDS', 'TDUP', 'TDW', 'TELL', 'TENB', 'TEX', 'TFIN', 'TFM', 'TG', 'TGAN', 'TGH', 'TGI', 'TGNA', 'TGTX', 'TH', 'THFF', 'THR', 'THRD', 'THRM', 'THRN', 'THRX', 'THRY', 'THS', 'TIL', 'TILE', 'TIPT', 'TITN', 'TK', 'TKNO', 'TLS', 'TLYS', 'TMCI', 'TMDX', 'TMHC', 'TMP', 'TMST', 'TNC', 'TNET', 'TNGX', 'TNK', 'TNYA', 'TOI', 'TOWN', 'TPB', 'TPC', 'TPH', 'TPIC', 'TR', 'TRC', 'TREE', 'TRMK', 'TRN', 'TRNO', 'TRNS', 'TROX', 'TRS', 'TRST', 'TRTN', 'TRTX', 'TRUE', 'TRUP', 'TSE', 'TSP', 'TSVT', 'TTCF', 'TTEC', 'TTGT', 'TTI', 'TTMI', 'TTSH', 'TUP', 'TVTX', 'TWI', 'TWNK', 'TWO', 'TWOU', 'TWST', 'TXRH', 'TYRA', 'UBA', 'UBSI', 'UCBI', 'UCTT', 'UDMY', 'UE', 'UEC', 'UEIC', 'UFCS', 'UFI', 'UFPI', 'UFPT', 'UHT', 'UIS', 'ULCC', 'ULH', 'UMBF', 'UMH', 'UNF', 'UNFI', 'UNIT', 'UNTY', 'UONE', 'UONEK', 'UP', 'UPBD', 'UPLD', 'UPWK', 'URBN', 'URG', 'USCB', 'USLM', 'USM', 'USNA', 'USPH', 'UTI', 'UTL', 'UTMD', 'UTZ', 'UUUU', 'UVE', 'UVSP', 'UVV', 'VAL', 'VALU', 'VBIV', 'VBTX', 'VC', 'VCEL', 'VCSA', 'VCTR', 'VCYT', 'VECO', 'VEL', 'VERA', 'VERI', 'VERU', 'VERV', 'VGR', 'VHI', 'VIA', 'VIAV', 'VICR', 'VIEW', 'VIR', 'VITL', 'VLD', 'VLGEA', 'VLY', 'VMEO', 'VNDA', 'VPG', 'VRAY', 'VRDN', 'VRE', 'VREX', 'VRNS', 'VRNT', 'VRRM', 'VRTS', 'VRTV', 'VSEC', 'VSH', 'VSTO', 'VTGN', 'VTLE', 'VTNR', 'VTOL', 'VTYX', 'VUZI', 'VVI', 'VVX', 'VWE', 'VXRT', 'VZIO', 'WABC', 'WAFD', 'WASH', 'WD', 'WDFC', 'WEAV', 'WERN', 'WEYS', 'WFRD', 'WGO', 'WGS', 'WHD', 'WINA', 'WING', 'WIRE', 'WISH', 'WK', 'WKHS', 'WLDN', 'WLLAW', 'WLLBW', 'WLY', 'WMK', 'WNC', 'WOR', 'WOW', 'WRBY', 'WRLD', 'WSBC', 'WSBF', 'WSFS', 'WSR', 'WT', 'WTBA', 'WTI', 'WTS', 'WTTR', 'WULF', 'WW', 'WWW', 'XERS', 'XHR', 'XMTR', 'XNCR', 'XOS', 'XPEL', 'XPER', 'XPOF', 'XPRO', 'XRX', 'XXII', 'YELP', 'YEXT', 'YMAB', 'YORW', 'YOU', 'ZD', 'ZETA', 'ZEUS', 'ZEV', 'ZGN', 'ZIMV', 'ZIP', 'ZNTL', 'ZUMZ', 'ZUO', 'ZWS', 'ZYXI']
    
    
    list_consolidated = []

    #function to check if the Stock has been consolidating for last 15 days
    def is_consolidating(ticker,df,percentage = 2):
        threshhold = 1 - (percentage / 100)
        recent_closes = df[-15:]['Close']
        recent_closes_max = recent_closes.max()
        recent_closes_min = recent_closes.min()
        
        if recent_closes_min > (recent_closes_max * threshhold):
            Cons_Dictionary = {'Ticker':ticker,'range':recent_closes_min/recent_closes_max}
            list_consolidated.append(Cons_Dictionary)

    # Email
    def send_mail(body):
        message = MIMEMultipart()
        message['Subject'] = 'Consolidating Stocks for the day'
        message['From'] = 'kc.milan.it@gmail.com'
        message['To'] = 'kc.milan.it@gmail.com'

        body_content = body
        message.attach(MIMEText(body_content, "html"))
        msg_body = message.as_string()

        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(message['From'], 'dzzlkoqqswozcdtl')
        server.sendmail(message['From'], message['To'], msg_body)
        server.quit()
    
    def send_consolidation_list():
        consolidated_stocks_df = pd.DataFrame.from_records(list_consolidated)
        consolidated_stocks_df.sort_values(by="range",ascending=True)
        output = build_table(consolidated_stocks_df, 'blue_light')
        send_mail(output)
    
    for ticker in ticker_list:
        start = dt.datetime.now() + dt.timedelta(days= -15) 
        now = dt.datetime.now()  
        data = yf.download(ticker, start=start, end=now)
        is_consolidating(ticker,data,2)
    
    send_consolidation_list()

main()

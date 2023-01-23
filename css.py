stylesheet = """
body {
	background-color: inherit; /* background color */
	color: inherit; /* text color */
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	margin: 0px 0px 0px 0px; /* top right bottom left */
}

.phpmaker {
	color: inherit; /* text color */
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */	
}

input, textarea, select {	
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
} 

a:active {
	color: #6C6C6C; /* active link color */
	text-decoration: none;
}

a:link {
	color: #6C6C6C; /* link color */
	text-decoration: none;
}

a:visited {
	color: #6C6C6C; /* visited link color */
   text-decoration: none;
}

a:hover {
	color: #990000; /* visited link color */
   text-decoration: underline;
}

/* main table */
.ewTable {
	width: auto; /* table width */	
	color: inherit; /* text color */
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	border: 0px outset; /* border */
	border-collapse: collapse;
}

/* main table data cells */
.ewTable td {
	padding: 4px; /* cell padding */
	border: 1px solid; /* cell spacing */
	border-color: #FFFFFF;  /* table background color */
}

.ewBasicSearch {
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	border: 0px;
	border-collapse: collapse;
}

.ewBasicSearch td {
	border: 0px;
	padding: 1px;
}

.ewSearchOpr {
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	color: maroon;
}

.ewListAdd {
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	border: 0px;
	border-collapse: collapse;
}

.ewListAdd td {
	border: 0px;
	padding: 2px;
}

.phpmakerlist td {
	color: inherit; /* text color */
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	border: 0px;
	padding: 0px;
	vertical-align: top; 
}

.ewAddOption td {
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	padding: 2px; /* cell padding */	
	border: 0px;	
}

/* main table header cells */
.ewTableHeader {
	background-color: E0E0E0; /* header color */
	color: #000000; /* header font color */	
	vertical-align: top;	
}

.ewTableHeader a:link {	
	color: #000000; /* header font color */	
}

.ewTableHeader a:visited {	
	color: #000000; /* header font color */	
}

/* main table row color */
.ewTableRow {
	background-color: #FFFFFF;  /* alt row color 1 */
}

/* main table alternate row color */
.ewTableAltRow {
	background-color: #F5F5F5; /* alt row color 2 */	
}

/* main table edit mode row color */
.ewTableEditRow {
	background-color: #DCDCDC; /* edit mode color */
}

/* main table highlight color */
.ewTableHighlightRow {
	background-color: #EAEAEA; /* highlight color */
}

/* main table select color */
.ewTableSelectRow {
	background-color: #EAEAEA; /* select color */
}

/* main table footer section */
.ewTableFooter {
	background-color: #DCDCDC;
}

/* classes for report */
.ewReportTable {
    border: 0px;
    border-collapse: collapse;
}

.ewReportTable td {
    padding: 3px;
}

.ewGroupField {
	font-weight: bold;
}

.ewGroupName {
	font-weight: bold;
}

.ewGroupHeader {
	border-bottom: 1px solid Black;
	border-top: 1px solid Black;
}

.ewGroupSummary {
	border-top: 1px solid Black;
} 

.ewGroupHeaderPortal {
	border-bottom: 1px solid White;
	border-top: 1px solid White;
}

.ewGroupSummaryPortal {
	border-top: 1px solid White;
} 

.ewGroupAggregate {
	font-weight: bold;
}

.ewGrandSummary {
	border-top: 1px solid Gray;
}

/* message */
.ewmsg {
	color: red; /* message color */
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */	
}

/* Ajax */
.ewAstList {
	border: 1px solid black;
	background: #ffffff;
	position: absolute;
	padding: 0;
	white-space: nowrap;
}

.ewAstListBase {
	position: absolute;
	padding: 1;
}

.ewAstListItem {
	color: black;
	background: #ffffff;
	cursor: hand;
	cursor: pointer;
	white-space: nowrap;
	padding: 1;
}

.ewAstSelListItem {
	color: white;
	background: Highlight;
	cursor: hand;
	cursor: pointer;
	white-space: nowrap;
	padding: 1;
}

/* MultiPage pager table */
.ewMultiPagePager {
	color: inherit; /* text color */
	font-family: Verdana; /* font name */
	font-size: 9pt; /* font size */
	border: 0px; /* border */	
}

.ewMultiPagePager td {
	padding: 2px; /* cell padding */	
}

/*END_SYSTEM_STYLES*/

"""

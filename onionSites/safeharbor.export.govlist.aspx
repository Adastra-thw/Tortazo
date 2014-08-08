

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head><link rel="stylesheet" type="text/css" href="CSS/SH_Styles.css" /><link rel="stylesheet" type="text/css" href="CSS/SH_Styles_Print.css" media="print" /><title>
	Safe Harbor - List
</title>

<script type="text/javascript" language="JavaScript" src="../JS/jquery.js"></script>
<script type="text/javascript">
    if (typeof jQuery != 'undefined') {
        jQuery(document).ready(function ($) {
            var filetypes = /\.(zip|exe|pdf|mp4|mov|wmv|txt|doc*|xls*|ppt*|mp3)$/i;
            var baseHref = '';
            if (jQuery('base').attr('href') != undefined)
                baseHref = jQuery('base').attr('href');
            jQuery('a').each(function () {
                var href = jQuery(this).attr('href');
                if (href && (href.match(/^https?\:/i)) && (!href.match(document.domain))) {
                    jQuery(this).click(function () {
                        var extLink = href.replace(/^https?\:\/\//i, '');
                        _gaq.push(['_trackEvent', 'External', 'Click', extLink]);
                        if (jQuery(this).attr('target') != undefined && jQuery(this).attr('target').toLowerCase() != '_blank') {
                            setTimeout(function () { location.href = href; }, 200);
                            return false;
                        }
                    });
                }
                else if (href && href.match(/^mailto\:/i)) {
                    jQuery(this).click(function () {
                        var mailLink = href.replace(/^mailto\:/i, '');
                        _gaq.push(['_trackEvent', 'Email', 'Click', mailLink]);
                    });
                }
                else if (href && href.match(filetypes)) {
                    jQuery(this).click(function () {
                        var extension = (/[.]/.exec(href)) ? /[^.]+$/.exec(href) : undefined;
                        var filePath = href;
                        _gaq.push(['_trackEvent', 'Download', 'Click-' + extension, filePath]);
                        if (jQuery(this).attr('target') != undefined && jQuery(this).attr('target').toLowerCase() != '_blank') {
                            setTimeout(function () { location.href = baseHref + href; }, 200);
                            return false;
                        }
                    });
                }
            });
        });
    } </script>

<script type="text/javascript">

    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-28628707-1']);
    _gaq.push(['_setDomainName', '.export.gov']);
    _gaq.push(['_trackPageview']);
    setTimeout("_gaq.push(['_trackEvent', '10_seconds', 'read'])", 10000);

    (function () {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();

</script>
<script type='text/javascript' src="../JS/foresee-trigger.js"></script>
<script type="text/javascript" src="../JS/federated-analytics.js"></script>



</head>
<body>
<form name="aspnetForm" method="post" action="list.aspx" id="aspnetForm">
<input type="hidden" name="ctl00_mainContent_ScriptManager1_HiddenField" id="ctl00_mainContent_ScriptManager1_HiddenField" value="" />
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="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" />


<script src="/ScriptResource.axd?d=kWl21SAvgDhJ9uQRvTmK8-ZH-NT0Bn0ouUqjLNgh2akIRI2s8PjIG9CTMhj_Eui7L7ljq1Oz8FdMijrS4kNQw2cN0mx2H77tzJQsmNPPRrScFW4a0&amp;t=ffffffffec54f2d7" type="text/javascript"></script>
<script src="/list.aspx?_TSM_HiddenField_=ctl00_mainContent_ScriptManager1_HiddenField&amp;_TSM_CombinedScripts_=%3b%3bAjaxControlToolkit%2c+Version%3d3.5.40412.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d28f01b0e84b6d53e%3aen-US%3a1547e793-5b7e-48fe-8490-03a375b13a33%3a5546a2b%3a475a4ef5%3ad2e10b12%3aeffe2a26%3af9e9a939" type="text/javascript"></script>
<input type="hidden" name="__VIEWSTATEENCRYPTED" id="__VIEWSTATEENCRYPTED" value="" />
<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="sauu+pRBF0bGWzvrTPJovapttvfNwcbnz6uw8Ok2qT6NkwmujAB4gSg61+ou5UOoLpuhZ/m3YOnNavAt3X73kenbNnWUAFEsCf/eCJgWRGZnwel+waMBB7KlbU/jGe80Df0YlbSThIqX7htgPqmSFcvY4BZdhH2wLvhY0OgA3dPnEedr3ReDldpy+XemKcQaKNIw0bzSZDw9OQ6mR4Xger3OLY7huMzc9sxMzcpY91jnjKBv7Vyux5FVHZ6EiWOaMG1NTZWgilFdvjD+BAwfS0fT0I5Tf7BPg1y9aUbTu1KyKnK33bK39H7Fah/TxXF0XjUxNPOG4iv+1UfXXoWgeb5KvQceosJfssouNbqyd84boWjAY+qL6lbOW9WwfMhfppMRtCFhhv136zQCiW90cRBM8mJeg8Ai+xMWOVFwXzZ0XeKZbyHM3NmHQFrF8sMKtyx+ExetVZVLbshLuW4nvGGMAIcBMGJf4Rr2Rt7nEtlkinTPI9P7rHpUsZ1ZUIuNrlyYQIBhcnv6JicrEg41tJvUQSXtksxGHr6VBtV0GjcjUrCJQviIAsYj6M30SvJzFn995JKHytKIIMk8/9JjY4wdNFvAl+4j3wY5eScOZIHrdFwnamnhqCUX1CyjxzHH5kKMQrUn/HkpmCyXUWvg4JBS/xCPokoinKAh4wWmF1F15EhCTXT0arPXWJutSy6sXEJmMHCWIlsnAiVU69X+8mWgeaVsl3KSjiWT4bjqGb4sb6Jf096s2/26pTYTk2gjJCs25IO9apPre7R0mZHT4/VXWuIQbul8S1IOwdRo+khmS3vpChrvSB14MPAFXlrwO9pqzYEiPvL0EKj74/J87MttBQckq2/9qO+0BxGGCFLa+aTv6VFxcy/x8PmpRUUdATVcBj2fKbMsSAKnIvSjy/ZD6KBYpDSuxAJU68HvVPqHZsLjB0kf+qv3M5ONZMwAXtH8atoktYzvvnlJ9dqSipSJohqa0ow0zyIqCJEFcLL/4ZX2Ti/MDVg0YgSD7B7iLmDLCAHrYu0+WihYTX/nAtR4853FDFN1EwoiR5Ce2hHfTRqvOoZZNHLduXmxpr1BAA8sdcVBT26VIanFumO/mXg8IgsNS0ujQUuk93IAVxDSegP4XkDz12aWUsc/U26hfz/uZ2gnJpj41sUh0M0zbE9uqMHwDCGephGd6OBbWL09d7ZSCYWizroPfVf124F+iLl0D5271JM6Odbp3u3NszvrcHs2cGmJJYh5/8kOlbt3oCbf3iXXrNtkUJlB92r9DSgP21JlnHdvRLTY2XkqV8UQcv7PkL3Qqo1ZKYzD/nCvxhCMpSNmdjmND434436hPsmOBOVRsEvXzlmffNL17xGq4w32trAvotres/enKQeJCAltHS418N84sLRNqDQfBpMaIW/0h+nUunK7HEdJfTkv8EHFbEf4CSQhYSJ8Jq+Rzb0a3h99ubavrSb+pmYt4aINgDUdt2pQPdsZrqDkVACp+v532tKeigBQKC8sw9oyA5G0IfsT8wNi+b2QxfhjDPuY7c2ljS+kpTscyFjFSQ15pthz1eszgV0KhrkNfwyVzESnCcLq83lAvFUT44W+xGfrsH/VczxUZ4alDDJ6dmNTbA9yce3cICK6/a5nQ9zRDlOULy3idj5K2tF97hd+Y0qUOyLzWIIbC3qhckN3O0PsIUEER4UYmfjfQVFCUFPeh1iDJFnhO6JKmZqVcg7wllBaKPieV874ZDXQGGZU1KlIOwM=" />
    <div class="framepagewidth"> 
    <!-- <div class="framethreecols">-->
    
     

  
    <div class="frameheader">      
	<div class="header">

	<div class="banner">
	    <img src="images/000588.jpg" alt="Export.gov - Helping U.S. Companies Export (text is in front of American flag)" border="0" />
	</div>
	<div class="cornerheader"><img id="ctl00_header1_Image4" src="images/000589.jpg" border="0" /></div>
	  	<div class="searchgoogle">
  				<div class="reg">
  				    <a id="ctl00_header1_hypRegister" href="register.aspx">Register</a>
  				    <span id="ctl00_header1_lblLine">|</span>  					
  				    <a id="ctl00_header1_hypLogin" href="login.aspx">Login</a>  					
  				</div>
	    </div>
    	
    <div class="topnav">
	    <div class="tnavtoplines"><img src="images/tnavtoplines.gif" height="2" width="780" border="0" /></div>
	    <div class="tnav">
		    <ul id="topnavigation">
			    <li><a id="ctl00_header1_HyperLink1" href="http://www.export.gov/nonuscompanies/index.asp">  Non-U.S. Companies  </a></li>
			    <li><a id="ctl00_header1_HyperLink2" href="http://www.export.gov/contactus/index.asp">  Contact Us  </a></li>
			    <li><a id="ctl00_header1_HyperLink3" href="http://export.gov/about/eg_main_019124.asp">  Partner Agencies  </a></li>
			    <li><a id="ctl00_header1_HyperLink4" href="http://www.export.gov/about/index.asp">  About Export.gov  </a></li>
			    <li><a id="ctl00_header1_HyperLink5" href="http://www.export.gov/safeharbor/">  Home  </a></li>
		    </ul>
	    </div>
	    <div class="tnavbottomlines"><img id="ctl00_header1_Image3" src="images/tnavbottomlines.gif" height="5" width="780" border="0" /></div>	    	    
    </div>    	        
</div>
</div>
 	   	
   
      <div class="frameleftcol">
          <div id="leftnav1">             
                
<div class="leftnav">
	<div class="sidesheadbkg">	    	
		<span class="sideshead">Find Opportunities</span>		
	</div>
	<div class="ls">
		<ul class="sides">
		<li><a id="ctl00_leftnav1_HyperLink1" href="http://www.export.gov/industry/index.asp">By Industry</a></li>
		<li><a id="ctl00_leftnav1_HyperLink2" href="http://www.export.gov/mrktresearch/index.asp">Market Research</a></li>
		<li><a id="ctl00_leftnav1_HyperLink3" href="http://www.export.gov/tradeevents/index.asp">Trade Events</a></li>
		<li><a id="ctl00_leftnav1_HyperLink4" href="http://www.export.gov/tradeleads/index.asp">Trade Leads</a></li>
		</ul>
	</div>
	<div class="sidesheadbkg">
		<span id="ctl00_leftnav1_Label1" class="sideshead">Find Solutions</span>		
	</div>
	 <div class="ls">
		<ul class="sides">
		<li><a id="ctl00_leftnav1_HyperLink5" href="http://www.export.gov/salesandmarketing/index.asp">International Sales-Marketing</a></li>
		<li><a id="ctl00_leftnav1_HyperLink6" href="http://www.export.gov/finance/index.asp">International Finance</a></li>
		<li><a id="ctl00_leftnav1_HyperLink7" href="http://www.export.gov/logistics/index.asp">International Logistics</a></li>
		<li><a id="ctl00_leftnav1_HyperLink8" href="http://www.export.gov/regulation/index.asp">Regulations & Licenses</a></li>
		<li><a id="ctl00_leftnav1_HyperLink9" href="http://www.export.gov/tradedata/index.asp">Trade Data & Analysis</a></li>
		<li><a id="ctl00_leftnav1_HyperLink10" href="http://www.export.gov/tradeproblems/index.asp">Trade Problems</a></li>
		</ul>
	</div>
	<div class="sidesheadbkg">
		<span id="ctl00_leftnav1_Label2" class="sideshead">Contact Us</span>		
	</div>

	<span id="ctl00_leftnav1_Label3" class="sides_no_ul">1-800-USA Trade</span>
	 
		<div class="ls">
		<ul class="sides">
		<li><a id="ctl00_leftnav1_HyperLink11" href="http://www.buyusa.gov/home/us.html">Find a Local U.S. Office</a></li>
		<li><a id="ctl00_leftnav1_HyperLink12" href="http://www.buyusa.gov/home/import.html" target="_blank">Find an Overseas Office</a></li>
		</ul>
		</div>
	<div class="sidescutcorner">

	</div>
</div>
          </div>
      </div>
      <div class="framemaincol2">
                
      
<div class="framerightcol">
<div class="righttop">
	<div class="printemail">
        <span id="ctl00_breadcrumbs1_lbluser"></span>
	    <span id="ctl00_breadcrumbs1_lbluserid"></span>	            
	    <a onclick="window.print();" id="ctl00_breadcrumbs1_linkprint" href="javascript:__doPostBack('ctl00$breadcrumbs1$linkprint','')">Print</a>
	    
	    
	    
	            
	</div>
</div>
</div>

           <div class="centerallcontent">
                <div id="main">                    
                    

    <div style="text-align:center;"><span class="heading">U.S.-EU SAFE HARBOR LIST</span></div>
    
    <ul id="ctl00_mainContent_BulletedList1">
	<li>The organizations on this list have notified the Department of Commerce that they adhere to the U.S.-EU Safe Harbor Framework developed by the Department of Commerce in coordination with the European Commission. The U.S.-EU Safe Harbor Framework provides guidance for U.S. organizations on how to provide adequate protection for personal data from the EU as required by the European Union's Directive on Data Protection.</li><li>An organization's self-certification of compliance with the U.S.-EU Safe Harbor Framework and the appearance of the organization on this list pursuant to the self-certification, constitute an enforceable representation to the Department of Commerce and the public that it adheres to a privacy policy that complies with the U.S.-EU Safe Harbor Framework.</li><li>There are benefits to organizations that participate in the U.S.-EU Safe Harbor program, but participation in the U.S.-EU Safe Harbor Framework and self-certification to the list are voluntary. Once an entity elects to participate in the program, it is legally required to comply with the Safe Harbor Privacy Principles. An organization's absence from the list does not mean that it does not provide effective protection for personal data or that it does not qualify for the benefits of the U.S.-EU Safe Harbor program. In order to keep this list current, a notification will be effective for a period of twelve months; therefore, organizations must notify the Department of Commerce every twelve months to reaffirm their continued adherence to the U.S.-EU Safe Harbor Framework.</li><li>Organizations should notify the Department of Commerce if their representation to the Department is no longer valid. Failure by an organization to so notify the Department could constitute a misrepresentation.</li><li>An organization may withdraw from the list at any time by notifying the Department of Commerce. Withdrawal from the list terminates the organization's representation of adherence to the U.S.-EU Safe Harbor Framework, but this does not relieve the organization of its Safe Harbor obligations with respect to personal information received during the time that the organization was on the U.S.-EU Safe Harbor list.</li><li>If a relevant self-regulatory or government enforcement body finds that an organization has engaged in a persistent failure to comply with the U.S.-EU Safe Harbor Privacy Principles, then that organization is no longer entitled to the benefits of the U.S.-EU Safe Harbor program. In this case, the organization must promptly notify the Department of Commerce of such facts either by email or letter. Failure to do so may be actionable under the False Statements Act (18 U.S.C. 1001). That organization must also provide the Department of Commerce with a copy of the decision letter from the relevant self-regulatory or government enforcement body.</li>
</ul>
    
    <div style="font-weight:bold; font-style:italic;">
    <ul id="ctl00_mainContent_BulletedList2">
	<li>In maintaining the list, the Department of Commerce does not assess and makes no representations to the adequacy of any organization's privacy policy or its adherence to that policy. Furthermore, the Department of Commerce does not guarantee the accuracy of the list and assumes no liability for the erroneous inclusion, misidentification, omission, or deletion of any organization, or any other action related to the maintenance of the list.</li>
</ul>
    </div>
   
            
    <div id="ctl00_mainContent_UP1">
	

    <input type="hidden" name="ctl00$mainContent$CollapsiblePanelExtender1_ClientState" id="ctl00_mainContent_CollapsiblePanelExtender1_ClientState" />

    <div id="ctl00_mainContent_PnlTitle" class="collapsePanelHeader">
		
        <img id="ctl00_mainContent_Image1" src="images/expand.jpg" border="0" />
        <span>Search by Organization Details </span>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <span id="ctl00_mainContent_Label5"><i>Show Details(...)</i></span>
    
	</div>

    
    <div id="ctl00_mainContent_pnlkeyword">
		
    <table>
    <tr>
    <td>
        <span id="ctl00_mainContent_Label2">Organization Name: </span>
    </td>
    <td>        
        <input name="ctl00$mainContent$txtcompanyname" type="text" id="ctl00_mainContent_txtcompanyname" />        
    </td>
    </tr>
    <tr>
    <td colspan="2">
        <span id="ctl00_mainContent_Label6"><font color="Blue">Search Tip: Enter either (a) the exact Organization Name (e.g. The XYZ Corporation); or (b) the % symbol immediately before (i.e. no space) a word of consequence from the Organization Name (e.g. %XYZ)</font></span>        
    </td>
    </tr>
    
    <tr >
    <td>
        <span id="ctl00_mainContent_Label3">Keyword: </span>        
    </td>        
    <td>
        <input name="ctl00$mainContent$txtKeyword" type="text" id="ctl00_mainContent_txtKeyword" />
    </td>        
    </tr>
    
    <tr>
    <td colspan="2">
        <span id="ctl00_mainContent_Label8"><font color="Blue">Search Tip: Enter the Organization Contact name, Corporate Officer name or Zip Code</font></span>                    
    </td>
    </tr>
        
    <tr >
    <td>
        <span id="ctl00_mainContent_Label11">Phrase: </span>        
    </td>        
    <td>
        <input name="ctl00$mainContent$txtExtactPhrase" type="text" id="ctl00_mainContent_txtExtactPhrase" />
    </td>        
    </tr>
    <tr>
    <td colspan="2">
        <span id="ctl00_mainContent_Label12"><font color="Blue">Search Tip: Enter a phrase or phrases enclosing each within quotation marks. Three types of phrase-based searches are possible: (1) a search for results containing a single phrase (e.g. “data protection authorities”); (2) a search for results containing all of the specified phrases (e.g. “data protection authorities” AND “DPAs”); and (3) a search for results containing any of the specified phrases (e.g. “data protection authorities” OR “DPAs”). This function is especially useful when searching for records that reference a particular Independent Recourse Mechanism or Verification Method.</font></span>                    
    </td>
    </tr>
    
    <tr>
    <td>
        <span id="ctl00_mainContent_lblsearch">Industry Sector: </span>    
    </td>
    <td>
        <select name="ctl00$mainContent$ddindsector" id="ctl00_mainContent_ddindsector">
			<option value=""></option>
			<option value="ACT">Accounting Services - (ACT)</option>
			<option value="ADV">Advertising Services - (ADV)</option>
			<option value="AGC">Agricultural Chemicals - (AGC)</option>
			<option value="AGM">Agricultural Machinery &amp; Equipment - (AGM)</option>
			<option value="AGS">Agricultural Services - (AGS)</option>
			<option value="ACR">Air Conditioning &amp; Refrigeration Equipment - (ACR)</option>
			<option value="AIR">Aircraft &amp; Parts - (AIR)</option>
			<option value="APG">Airport &amp; Ground Support Equipment - (APG)</option>
			<option value="APP">Apparel - (APP)</option>
			<option value="ACE">Architectural/Construction/Eng Svc - (ACE)</option>
			<option value="ARW">Artwork - (ARW)</option>
			<option value="AUV">Audio/Visual Equipment - (AUV)</option>
			<option value="AUT">Automobiles &amp; Light Trucks/Vans - (AUT)</option>
			<option value="APS">Automotive Parts &amp; Service Equipment - (APS)</option>
			<option value="AVS">Aviation Services - (AVS)</option>
			<option value="BTC">Biotechnology - (BTC)</option>
			<option value="BOK">Books &amp; Periodicals - (BOK)</option>
			<option value="BLD">Building Products - (BLD)</option>
			<option value="BUS">Business Eqpt (other than computers) - (BUS)</option>
			<option value="CRM">Ceramics Fine Advanced - (CRM)</option>
			<option value="CHM">Chemical Production Machinery - (CHM)</option>
			<option value="COL">Coal - (COL)</option>
			<option value="CVR">Comm Vessels &amp; Eqpt (EXCL FISH) - (CVR)</option>
			<option value="CFE">Commercial Fishing Equipment - (CFE)</option>
			<option value="CMT">Composite Materials - (CMT)</option>
			<option value="CPT">Computer &amp; Peripherals - (CPT)</option>
			<option value="CSV">Computer Services - (CSV)</option>
			<option value="CSF">Computer Software - (CSF)</option>
			<option value="CON">Construction Equipment - (CON)</option>
			<option value="CEL">Consumer Electronics - (CEL)</option>
			<option value="COS">Cosmetics &amp; Toiletries - (COS)</option>
			<option value="DFN">Defense Industry Equipment - (DFN)</option>
			<option value="DNT">Dental Equipment - (DNT)</option>
			<option value="DRG">Drugs &amp; Pharmaceuticals - (DRG)</option>
			<option value="EDS">Education &amp; Training - (EDS)</option>
			<option value="ELP">Electrical Power Systems - (ELP)</option>
			<option value="ELC">Electronic Components - (ELC)</option>
			<option value="EIP">Electronics Industry Prod/Test Equipment - (EIP)</option>
			<option value="EMP">Employment Services - (EMP)</option>
			<option value="FLM">Films Videos &amp; Other Recordings - (FLM)</option>
			<option value="FNS">Financial Services - (FNS)</option>
			<option value="FPP">Food Processing &amp; Packaging Eqpt - (FPP)</option>
			<option value="FOD">Foods Processed - (FOD)</option>
			<option value="FOT">Footwear - (FOT)</option>
			<option value="FOR">Forestry &amp; Woodworking Machinery - (FOR)</option>
			<option value="FUR">Furniture - (FUR)</option>
			<option value="GCG">General Consumer Goods - (GCG)</option>
			<option value="GIE">General Industrial Eqpt &amp; Supplies - (GIE)</option>
			<option value="GST">General Science &amp; Technology - (GST)</option>
			<option value="GSV">General Services - (GSV)</option>
			<option value="GFT">Giftware - (GFT)</option>
			<option value="HCS">Health Care Services - (HCS)</option>
			<option value="HTL">Hotel &amp; Restaurant Equipment - (HTL)</option>
			<option value="HCG">Household Consumer Goods - (HCG)</option>
			<option value="ICH">Industrial Chemicals - (ICH)</option>
			<option value="INF">Information Services - (INF)</option>
			<option value="INS">Insurance Services - (INS)</option>
			<option value="INV">Investment Service - (INV)</option>
			<option value="IRN">Iron &amp; Steel - (IRN)</option>
			<option value="JLR">Jewelry - (JLR)</option>
			<option value="LAB">Laboratory Scientific Instruments - (LAB)</option>
			<option value="LGE">Lawn &amp; Garden Equipment - (LGE)</option>
			<option value="LES">Leasing Services - (LES)</option>
			<option value="LFP">Leather &amp; Fur Products - (LFP)</option>
			<option value="LSE">Legal Services - (LES)</option>
			<option value="MTL">Machine Tools &amp; Metal Working Eqpt - (MTL)</option>
			<option value="MCS">Management Consulting Services - (MCS)</option>
			<option value="MFI">Marine Fish Products - (MFI)</option>
			<option value="MED">Medical Equipment - (MED)</option>
			<option value="MIN">Mining Industry Equipment - (MIN)</option>
			<option value="MUS">Musical Instruments - (MUS)</option>
			<option value="NFM">Non-Ferrous Metals - (NFM)</option>
			<option value="OGM">Oil &amp; Gas Field Machinery - (OGM)</option>
			<option value="OGS">Oil Gas Mineral -(OGS)
Oil Gas Mineral Production</option>
			<option value="PKG">Packaging Eqpt (other than food) - (PKG)</option>
			<option value="PAP">Paper &amp; Paperboard - (PAP)</option>
			<option value="PET">Pet Foods &amp; Supplies - (PET)</option>
			<option value="PHT">Photographic Equipment - (PHT)</option>
			<option value="PMR">Plastic Materials &amp; Resin - (PMR)</option>
			<option value="PME">Plastics Production Machinery - (PME)</option>
			<option value="PLB">Pleasure Boats &amp; Accessories - (PLB)</option>
			<option value="POL">Pollution Control Equipment - (POL)</option>
			<option value="PRT">Port &amp; Shipbuilding Equipment - (PRT)</option>
			<option value="PGA">Printing &amp; Graphic Arts Equipment - (PGA)</option>
			<option value="PCI">Process Controls Industrial - (PCI)</option>
			<option value="PUL">Pulp &amp; Paper Machinery - (PUL)</option>
			<option value="PVC">Pumps Valves &amp; Compressors - (PVC)</option>
			<option value="RRE">Railroad Equipment - (RRE)</option>
			<option value="REQ">Renewable Energy Equipment - (REQ)</option>
			<option value="ROB">Robotics - (ROB)</option>
			<option value="SEC">Security &amp; Safety Equipment - (SEC)</option>
			<option value="SPT">Sporting Goods &amp; Recreational Equipment - (SPT)</option>
			<option value="TEL">Telecommunications Equipment - (TEL)</option>
			<option value="TES">Telecommunications Services - (TES)</option>
			<option value="TXF">Textile Fabrics - (TXF)</option>
			<option value="TXM">Textile Machinery &amp; Equipment - (TXM)</option>
			<option value="TXP">Textile Products - (TXP)</option>
			<option value="TLS">Tools Hand &amp; Power - (TLS)</option>
			<option value="TOY">Toy &amp; Games - (TOY)</option>
			<option value="TRN">Transportation Srvs (Except Aviation) - (TRN)</option>
			<option value="TRA">Travel &amp; Tourism Services - (TRA)</option>
			<option value="TRK">Trucks Trailers &amp; Buses - (TRK)</option>
			<option value="USD">Used &amp; Reconditioned Equipment - (USD)</option>
			<option value="VET">Veterinary Equipment &amp; Supplies - (VET)</option>
			<option value="WRE">Water Resources Eqpt &amp; Services - (WRE)</option>
			<option value="YAR">Yarns - (YAR)</option>

		</select>    
    </td>
    </tr>
    <tr >
    <td>
        <span id="ctl00_mainContent_Label1">State: </span>    
    </td>
    <td>
        <select name="ctl00$mainContent$ddstate" id="ctl00_mainContent_ddstate">
			<option value=""></option>
			<option value="AL">Alabama</option>
			<option value="AK">Alaska</option>
			<option value="AZ">Arizona</option>
			<option value="AR">Arkansas</option>
			<option value="CA">California</option>
			<option value="CO">Colorado</option>
			<option value="CT">Connecticut</option>
			<option value="DE">Delaware</option>
			<option value="DC">District of Columbia</option>
			<option value="FL">Florida</option>
			<option value="GA">Georgia</option>
			<option value="HI">Hawaii</option>
			<option value="ID">Idaho</option>
			<option value="IL">Illinois</option>
			<option value="IN">Indiana</option>
			<option value="IA">Iowa</option>
			<option value="KS">Kansas</option>
			<option value="KY">Kentucky</option>
			<option value="LA">Louisiana</option>
			<option value="ME">Maine</option>
			<option value="MD">Maryland</option>
			<option value="MA">Massachusetts</option>
			<option value="MI">Michigan</option>
			<option value="MN">Minnesota</option>
			<option value="MS">Mississippi</option>
			<option value="MO">Missouri</option>
			<option value="MT">Montana</option>
			<option value="NE">Nebraska</option>
			<option value="NV">Nevada</option>
			<option value="NH">New Hampshire</option>
			<option value="NJ">New Jersey</option>
			<option value="NM">New Mexico</option>
			<option value="NY">New York</option>
			<option value="NC">North Carolina</option>
			<option value="ND">North Dakota</option>
			<option value="NA">Not Assigned</option>
			<option value="OH">Ohio</option>
			<option value="OK">Oklahoma</option>
			<option value="OR">Oregon</option>
			<option value="PA">Pennsylvania</option>
			<option value="PR">Puerto Rico</option>
			<option value="RI">Rhode Island</option>
			<option value="SC">South Carolina</option>
			<option value="SD">South Dakota</option>
			<option value="TN">Tennessee</option>
			<option value="TX">Texas</option>
			<option value="UT">Utah</option>
			<option value="VT">Vermont</option>
			<option value="VA">Virginia</option>
			<option value="WA">Washington</option>
			<option value="WV">West Virginia</option>
			<option value="WI">Wisconsin</option>
			<option value="WY">Wyoming</option>

		</select>    
    </td>
    </tr>
    <tr>
    <td></td>
    <td>
        <input type="submit" name="ctl00$mainContent$btnKeywordSearch" value="Search" id="ctl00_mainContent_btnKeywordSearch" />
    
    </td>    
    </tr>
     

    </table>
    
	</div>  
    
    <br />                

    <input type="hidden" name="ctl00$mainContent$CollapsiblePanelExtender2_ClientState" id="ctl00_mainContent_CollapsiblePanelExtender2_ClientState" />

    <div id="ctl00_mainContent_pnlCertStatusTitle" class="collapsePanelHeader">
		
        <img id="ctl00_mainContent_Image2" src="images/expand.jpg" border="0" />
        <span id="ctl00_mainContent_Label4">Search by Organization Certification Status</span>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <span id="ctl00_mainContent_Label9"><i>Show Details(...)</i></span>
    
	</div>
    
    <div id="ctl00_mainContent_pnlCertStatus">
		    
    <table>
    <tr>
    <td>
        <span id="ctl00_mainContent_Label10">Certification Status: </span>    
    </td>
    <td>
        <select name="ctl00$mainContent$ddCertStatus" id="ctl00_mainContent_ddCertStatus">
			<option selected="selected" value=""></option>
			<option value="1">Current</option>
			<option value="2">Not Current</option>

		</select>    
    </td>
    </tr> 
    <tr>
    <td colspan="2">
        <span id="ctl00_mainContent_Label13"><font color="Blue">Notice:  An organization may be designated as “Not Current” for a variety of reasons.  The most common reason is that the organization has failed to reaffirm its adherence to the Safe Harbor Privacy Principles on an annual basis as required by the Safe Harbor Frameworks.  Another possible reason is that the organization has failed to comply with one or more of the Safe Harbor Privacy Principles.  Organizations designated as “Not Current” are no longer assured of the benefits of the Safe Harbor (i.e., the presumption of “adequacy”).  These organizations nevertheless must continue to apply the Safe Harbor Privacy Principles to the personal data received during the period in which they were assured of the benefits of the Safe Harbor for as long as they store, use or disclose those data.  Any misrepresentation by an organization designated as “Not Current” concerning its adherence to the Safe Harbor Privacy Principles may be actionable by the Federal Trade Commission or other relevant government body.</font></span>                    
    </td>
    </tr>     
    </table>  
    
	</div>    
   <br />
    <input type="hidden" name="ctl00$mainContent$CollapsiblePanelExtender3_ClientState" id="ctl00_mainContent_CollapsiblePanelExtender3_ClientState" />

    <div id="ctl00_mainContent_pnlCompanyInitialTitle" class="collapsePanelHeader">
		
        <img id="ctl00_mainContent_Image3" src="images/expand.jpg" border="0" />
        <span>Search Alphabetically for Organization Name</span>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <span id="ctl00_mainContent_Label7"><i>Show Details(...)</i></span>
    
	</div>
    
    <div id="ctl00_mainContent_pnlCompanyInitial">
		    
    <br />
    <div style="text-align:center;">
    <a id="ctl00_mainContent_LinkButton1" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton1','')">A</a>
    <a id="ctl00_mainContent_LinkButton2" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton2','')">B</a>
    <a id="ctl00_mainContent_LinkButton3" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton3','')">C</a>
    <a id="ctl00_mainContent_LinkButton4" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton4','')">D</a>
    <a id="ctl00_mainContent_LinkButton5" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton5','')">E</a>
    <a id="ctl00_mainContent_LinkButton6" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton6','')">F</a>
    <a id="ctl00_mainContent_LinkButton7" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton7','')">G</a>
    <a id="ctl00_mainContent_LinkButton8" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton8','')">H</a>
    <a id="ctl00_mainContent_LinkButton9" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton9','')">I</a>
    <a id="ctl00_mainContent_LinkButton10" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton10','')">J</a>
    <a id="ctl00_mainContent_LinkButton11" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton11','')">K</a>
    <a id="ctl00_mainContent_LinkButton12" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton12','')">L</a>
    <a id="ctl00_mainContent_LinkButton13" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton13','')">M</a>
    <a id="ctl00_mainContent_LinkButton14" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton14','')">N</a>
    <a id="ctl00_mainContent_LinkButton15" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton15','')">O</a>
    <a id="ctl00_mainContent_LinkButton16" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton16','')">P</a>
    <a id="ctl00_mainContent_LinkButton17" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton17','')">Q</a>
    <a id="ctl00_mainContent_LinkButton18" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton18','')">R</a>
    <a id="ctl00_mainContent_LinkButton19" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton19','')">S</a>
    <a id="ctl00_mainContent_LinkButton20" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton20','')">T</a>
    <a id="ctl00_mainContent_LinkButton21" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton21','')">U</a>
    <a id="ctl00_mainContent_LinkButton22" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton22','')">V</a>
    <a id="ctl00_mainContent_LinkButton23" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton23','')">W</a>
    <a id="ctl00_mainContent_LinkButton24" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton24','')">X</a>
    <a id="ctl00_mainContent_LinkButton25" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton25','')">Y</a>
    <a id="ctl00_mainContent_LinkButton26" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton26','')">Z</a>
    <a id="ctl00_mainContent_LinkButton27" class="searhalphabet" href="javascript:__doPostBack('ctl00$mainContent$LinkButton27','')">ALL</a>
    </div>
    <br />
    
	</div>
    <br />     
     <div style="text-align:center;"></div>  
     <div style="padding-bottom:25px">
     <div style="float:left;">
     <input type="image" name="ctl00$mainContent$ibExportToExcel" id="ctl00_mainContent_ibExportToExcel" title="Export to Excel" src="images/ExcelIcon.jpg" alt="Export to Excel" border="0" />     </div>
     <div style="float:right; font-weight:bold; padding-right:10px;"><span id="ctl00_mainContent_lblRecordCount">4753  Results</span></div>
     </div>   
     <div class="grid">
     <div>
		<table class="datatable" cellspacing="0" border="0" id="ctl00_mainContent_gridviewsafeharborlist" style="margin-left: 0px">
			<tr bgcolor="#507CD1">
				<th class="first" scope="col"><font color="White"><b><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Sort$sh_company')"><font color="White">Organization</font></a></b></font></th><th scope="col"><font color="White"><b><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Sort$sh_certstatusdesc')"><font color="White">Certification Status</font></a></b></font></th><th scope="col"><font color="White"><b><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Sort$sh_personaldata')"><font color="White">Personal Data</font></a></b></font></th>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=18752" target="_blank">@ legal discovery LLC</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">All personal data/On-line/On-line</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=16234" target="_blank">1-800-HOSTING, Inc.</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">off-line, on-line, manually processed data</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=7959" target="_blank">100 Spears, LLC d/b/a eWork</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">On-line, off-line, human resource data</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=8317" target="_blank">101 Distribution</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">on-line, off-line</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=19099" target="_blank">1010data Global Telecom Solutions LLC</a></td><td width="80">Current</td><td width="240">All personal information subject to the U.S.-EU Safe Harbor Privacy Principles.</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23530" target="_blank">101domain, Inc</a></td><td width="80">Current</td><td width="240">Data collected directly on the Internet; Data collected manually via paper, phone, or tradeshows.</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=20861" target="_blank">12 Forward Entertainment, LLC</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">No</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=6086" target="_blank">1992 International Ltd., dba, Sutton Associates</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">all employment screening matters</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=21090" target="_blank">1WorldSync, Inc.</a></td><td width="80">Current</td><td width="240">Personal information received about individual contacts of former, current and prospective customers.</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=22421" target="_blank">20/20 Software, Inc.</a></td><td width="80">Current</td><td width="240">Customer name, Company name, Address, Telephone, Email</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=19908" target="_blank">2020 Research</a></td><td width="80">Current</td><td width="240">Market research data primarily dealing with consumer research.</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=20038" target="_blank">247 customer, Inc.</a></td><td width="80">Current</td><td width="240">Data collected through [24]7 predictive experience platform includes information collected through our services offered to our clients as a Software as a solution provider. The data collected can include Online, offline, chat data etc.</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23983" target="_blank">2Checkout.com, Inc.</a></td><td width="80">Current</td><td width="240">Personal Data of clients and their customers that is processed on-line, off-line and manually</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=20446" target="_blank">2sms</a></td><td width="80">Current</td><td width="240">online data, manually processed data.</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23197" target="_blank">2Wire, Inc. d/b/a Pace Americas</a></td><td width="80">Current</td><td width="240">The personal data transferred may include the IP address of the device.  This information will be maintained primarily in an online database restricted to the use of Pace Americas and its corporate customers, and Pace Americas will maintain backups of this data offline.  The data processed will not include any manually processed data or human resources data.</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=22714" target="_blank">3 Story Software</a></td><td width="80">Current</td><td width="240">Off-line, on-line, manually processed data, human resources data.</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23565" target="_blank">3Cinteractive, LLC</a></td><td width="80">Current</td><td width="240">Personal identifiable information, UID</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23374" target="_blank">3D Systems Corporation</a></td><td width="80">Current</td><td width="240">Human Resources Data</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=22962" target="_blank">3d Travel Metrics</a></td><td width="80">Current</td><td width="240">off-line, on-line, manually processed data</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=22675" target="_blank">3dna Corporation, Inc. dba NationBuilder</a></td><td width="80">Current</td><td width="240">Consumer data, digitally processed.</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=19760" target="_blank">3G SELLING LLC</a></td><td width="80">Current</td><td width="240">Client/Customer contact information such as name, email address, mailing address, phone number.  Information about their business such as company name, company size, business type.  May be online or data received offline.</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=9321" target="_blank">3LZ International Corporation</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">online</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=22652" target="_blank">41st Parameter</a></td><td width="80">Current</td><td width="240">Online</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23651" target="_blank">4imprint Inc</a></td><td width="80">Current</td><td width="240">Customer name and address and information related to their purchases.</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=24051" target="_blank">4Thought Marketing</a></td><td width="80">Current</td><td width="240">Organization, Client, Customer</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=20782" target="_blank">500friends, Inc</a></td><td width="80">Current</td><td width="240">customer loyalty program data including email address, transaction history, loyalty program login credentials.  We do not process or store payment information.</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=22300" target="_blank">6Sense Insights</a></td><td width="80">Current</td><td width="240">Information received from customers, prospective customers and suppliers.</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=6090" target="_blank">780 Inc.</a></td><td width="80"><font color="Red">Not Current</font></td><td width="240">On-Line</td>
			</tr><tr class="row" bgcolor="#EFF3FB">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23233" target="_blank">7th Sense Limited Partnership</a></td><td width="80">Current</td><td width="240">Organization, client and consumer.  Consumer data includes phone numbers, email addresses and addresses. The data covered does not include manually processed data.</td>
			</tr><tr class="row" bgcolor="White">
				<td class="first" align="left" width="250"><a href="companyinfo.aspx?id=23400" target="_blank">81qd</a></td><td width="80">Current</td><td width="240">All personal information received</td>
			</tr><tr align="center" bgcolor="#2461BF">
				<td colspan="3"><font color="White"><table border="0">
					<tr>
						<td><font color="White"><span>1</span></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$2')"><font color="White">2</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$3')"><font color="White">3</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$4')"><font color="White">4</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$5')"><font color="White">5</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$6')"><font color="White">6</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$7')"><font color="White">7</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$8')"><font color="White">8</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$9')"><font color="White">9</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$10')"><font color="White">10</font></a></font></td><td><font color="White"><a href="javascript:__doPostBack('ctl00$mainContent$gridviewsafeharborlist','Page$11')"><font color="White">...</font></a></font></td>
					</tr>
				</table></font></td>
			</tr>
		</table>
	</div>
     </div>
     
</div>    

                </div>
           </div>       
       </div>
        <div>
            
      <div class="framefooter">
            <div class="footer">
	   		<div class="footerlines"></div>
			<div class="footercut">
				<div class="footertext">
				            <a id="ctl00_footer1_HyperLink1" href="http://www.export.gov/forms/exp_feedback_user.asp?URL=http://www.export.gov/">Submit Feedback</a>
				            |				         
							<a id="ctl00_footer1_HyperLink2" href="http://www.export.gov/about/eg_main_016803.asp">Privacy Policy Feedback</a>
               				|
                            <a id="ctl00_footer1_HyperLink3" href="http://www.export.gov/about/eg_main_016805.asp">Disclaimer</a>               				
                            |               				
                            <a id="ctl00_footer1_HyperLink4" href="http://www.usa.gov">USA.gov</a>               				
               				|
                            <a id="ctl00_footer1_HyperLink5" href="http://www.export.gov/articles/eg_main_016980.asp">Site Map</a>               				               				
                            |
                            <a id="ctl00_footer1_HyperLink6" href="http://www.adobe.com/products/acrobat/readstep2.html">Download Adobe Reader</a>               				               				               				
				</div>
			</div>	   
	   </div>			
      </div>
 
        </div>
       </div>
    

<script type="text/javascript">
//<![CDATA[
(function() {var fn = function() {$get("ctl00_mainContent_ScriptManager1_HiddenField").value = '';Sys.Application.remove_init(fn);};Sys.Application.add_init(fn);})();Sys.Application.initialize();
Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CollapsiblePanelBehavior, {"ClientStateFieldID":"ctl00_mainContent_CollapsiblePanelExtender1_ClientState","CollapseControlID":"ctl00_mainContent_PnlTitle","CollapsedImage":"images/expand.jpg","CollapsedText":"Show Details (...)","ExpandControlID":"ctl00_mainContent_PnlTitle","ExpandedImage":"images/collapse.jpg","ExpandedText":"Hide Details (...)","ImageControlID":"ctl00_mainContent_Image1","TextLabelID":"ctl00_mainContent_Label5","id":"ctl00_mainContent_CollapsiblePanelExtender1"}, null, null, $get("ctl00_mainContent_pnlkeyword"));
});
Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CollapsiblePanelBehavior, {"ClientStateFieldID":"ctl00_mainContent_CollapsiblePanelExtender2_ClientState","CollapseControlID":"ctl00_mainContent_pnlCertStatusTitle","CollapsedImage":"images/expand.jpg","CollapsedText":"Show Details (...)","ExpandControlID":"ctl00_mainContent_pnlCertStatusTitle","ExpandedImage":"images/collapse.jpg","ExpandedText":"Hide Details (...)","ImageControlID":"ctl00_mainContent_Image2","TextLabelID":"ctl00_mainContent_Label9","id":"ctl00_mainContent_CollapsiblePanelExtender2"}, null, null, $get("ctl00_mainContent_pnlCertStatus"));
});
Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CollapsiblePanelBehavior, {"ClientStateFieldID":"ctl00_mainContent_CollapsiblePanelExtender3_ClientState","CollapseControlID":"ctl00_mainContent_pnlCompanyInitialTitle","CollapsedImage":"images/expand.jpg","CollapsedText":"Show Details (...)","ExpandControlID":"ctl00_mainContent_pnlCompanyInitialTitle","ExpandedImage":"images/collapse.jpg","ExpandedText":"Hide Details (...)","ImageControlID":"ctl00_mainContent_Image3","TextLabelID":"ctl00_mainContent_Label7","id":"ctl00_mainContent_CollapsiblePanelExtender3"}, null, null, $get("ctl00_mainContent_pnlCompanyInitial"));
});
//]]>
</script>
</form>
</body>
</html>

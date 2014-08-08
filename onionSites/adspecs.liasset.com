<!doctype html>

<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!-->
<html lang="en" class="no-js">
<!--<![endif]-->
<head>
<meta charset="utf-8">
<title>Advertising Specifications | LinkedIn</title>
 <link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon-precomposed" href="/apple-touch-icon.png">
<link rel="stylesheet" type="text/css" href="/assets/css/adspecs.css?r=28443" media="screen">
<link rel="stylesheet" type="text/css" href="/assets/css/adspecs-print.css?r=28443" media="print">
<link rel="stylesheet" href="/assets/css/thickbox.css?r=28443" type="text/css" media="screen" />
<script type="text/javascript" src="http://www.liasset.com/_util/assets/js/build/modernizr-1.6.min.js"></script>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type="text/javascript">
	!window.jQuery && document.write(unescape('%3Cscript src="http://www.liasset.com/_util/assets/js/build/jquery-1.4.2.min.js"%3E%3C/script%3E'));
</script></head>

<body id="index">
<p class="not_supported"><strong>This site does not support Internet Explorer 6.</strong> Please <a href="http://www.microsoft.com/windows/internet-explorer/" rel="external">upgrade</a> or use <a href="http://browsehappy.com/" rel="external">an alternate browser</a>.</p>
<header>
  <div id="header">
    <h1> <a href="http://adspecs.linkedincreatives.com/"><span>LinkedIn</span> Advertising Specifications</a></h1>
    <nav>
      <ul class="nav">
        <li><a rel="external" href="http://marketing.linkedin.com/?trk=en-all-site-li-mktag-site&amp;utm_source=adspecs&amp;utm_medium=adspecs&amp;utm_content=adspecs&amp;utm_campaign=adspecs">Marketing Solutions</a></li>
        <li><a rel="external" href="https://www.linkedin.com/directads/start?trk=en-all-site-li-mktag-site&amp;utm_source=mktgsite&amp;utm_medium=mktgsite&amp;utm_content=adspecs&amp;utm_campaign=2011">LinkedIn Ads</a></li>
        <li><a rel="external" href="http://www.linkedin.com/"><strong>LinkedIn.com</strong></a></li>
      </ul>
    </nav>
  </div>
</header><div id="body">
  <div id="content" class="panels">
    <ul id="specs-nav" class="nav">
      <li><a href="/" class="selected">Specs</a>
  <ul class="specs-sub-nav nav"><li><a href="/">Common Specs</a></li><li><a href="/category.php?category=Content+Ads">Content Ads</a></li><li><a href="/category.php?category=Sponsored+InMail">Sponsored InMail</a></li><li><a href="/category.php?category=Sponsored+Updates">Sponsored Updates</a></li><li><a href="/category.php?category=Social+Ads">Social Ads</a></li><li><a href="/category.php?category=Polls">Polls</a></li></ul> 
      </li>
      <!--li>Resources</li-->
      <!--li><a href="/">Context</a></li-->
    </ul>    <div class="content">
      <h2>Common Advertising Specifications</h2>
      <div class="actions" id="page-actions"><!--a href="/assets/linkedin-adspecs-2011-1-0.pdf"><em>Download All Ad Specs (PDF)</em></a--></div>
      <div class="spec purpose">
        <p>These are the specifications for LinkedIn-approved formats.</p>
        <h4><span id="OLK_SRC_BODY_SECTION"><strong>SSL capability is now required:</strong></span> <span> LinkedIn requires that ads, creatives and tracking elements are requested using a secure connection (https).</span>        </h4>
        <p><span id="OLK_SRC_BODY_SECTION">More details: Starting immediately, LinkedIn pages   will be loaded over a secure connection. Secure connections (https) are   achieved using SSL (Secure Sockets Layer), which is the standard   security technology. To avoid warning messages   in the user's browser, we require that ads, creatives and tracking   elements are requested using a secure connection. Additionally, all   subsequent requests to media assets or tracking URLs must also use a   secure connection (<a href="https://email.corp.linkedin.com/owa/UrlBlockedError.aspx" target="_blank">HTTPS://</a>).   The only part of an ad permitted to be non-SSL compliant is the click URL (target landing page).</span> 
</p>
        <p>&nbsp; </p>
        <h4>General Information</h4>
        <ul>
          <li>We accept IFRAME/Javascript tags.</li>
          <li>We accept in-banner surveys &ndash; no floating layers or pop-ups.</li>
          <li>3rd party tags must be allowed for click tracking by our ad server via a click URL macro or redirect.</li>
          <li>All creative must function uniformly on both MAC and PC formats as well as multiple browser versions of Firefox, Internet Explorer, Safari, and Chrome.</li>
          <li>We do not allow the setting of "Flash cookies" (also known as LSO - Local Shared Objects).</li>
          <li>Please notify LinkedIn before making creative swap. Campaigns running creatives which do not meet spec may be paused.</li>
        </ul>
        <div id="index_detail" class="spec-detail">
          <h4>Creative Submission</h4>
          <ul>
            <li>All ads, including those running through third party code, must be submitted to LinkedIn for approval</li>
            <li>Standard ads &ndash; three (3) business days</li>
            <li>Rich media ads &ndash; five (5) business days</li>
            <li>Premium positions &amp; Sponsorships &ndash; seven (7) business days</li>
            <li>Third party servers should contact LinkedIn at least one (1) business day before rotating new ads into an existing ad campaign and provide those new ads for review.</li>
            <li>Submit all creative to your assigned Account Manager.</li>
          </ul>
          <h4>Inadmissible Advertising</h4>
          <ul>
            <li>Pop-ups and Pop-unders</li>
            <li>Floating ads or Floating layers.</li>
            <li>Please see our <a href="https://www.linkedin.com/legal/pop/pop-sas-guidelines" target="_blank">LinkedIn Advertising Guidelines</a> to determine whether your ad is appropriate for LinkedIn.</li>
          </ul>
          <!--p>Any questions related to LinkedIn Ad Specs, please <a href="/resource.php?resource=contact&amp;name=Contact+Advertising+Operations">contact us.</a></p-->
        </div>
        <a href="javascript:void(0);" class="more-less" id="index_toggle">details</a> </div>
            <div class="spec">
        <h3>
          160x600        </h3>
        <div class="actions"><a href="/detailed-spec.php?spec=all_160x600&amp;name=all_160x600" class="btn-ternary">Detailed Spec</a> <a title="160x600" href="/assets/images/tn/160x600.jpg" class="thickbox btn-quaternary">View in Page</a> <a href="/detailed-spec.php?spec=all_160x600&amp;name=all_160x600&amp;print=true" class="print" title="Print">Print</a></div>
        <table>
  <caption>
  * border required only with white and transparent backgrounds<br>
  ** 30 seconds is the total maximum length of all animation, including all loops</caption>
  <tr>
    <th>Regions</th>
    <td>Global</td>
    <th>Dimensions</th>
    <td>160x600</td>
  </tr>
  <tr>
    <th><abbr title="Interactive Advertising Bureau">IAB</abbr> Name</th>
    <td>Wide Skyscraper</td>
    <th>File Types</th>
    <td>GIF, JPG, PNG, SWF</td>
  </tr>
  <tr>
    <th>Size Limit</th>
    <td>40kb</td>
    <th>Border*</th>
    <td>1px*</td>
  </tr>
  <tr>
    <th>Rich Media Options</th>
    <td>Yes</td>
    <th>Animation Limit**</th>
    <td>15 sec for video quality autoplay<br />
    30 seconds otherwise**</td>
  </tr>
  <tr>
    <th>Video/Audio</th>
    <td>On user click</td>
    <th>3rd Party Tracking</th>
    <td>Yes</td>
  </tr>
  <tr>
    <th>Polite Download SWF Max</th>
    <td>100kb</td>
    <th>Polite Download Video Max</th>
    <td>2.2mb</td>
  </tr>
  <tr>
    <th>Ad Expand Direction &amp; Area</th>
    <td>Left - 480x600</td>
    <th></th>
    <td></td>
  </tr>
</table>
<div id="all_160x600_detail" class="spec-detail">
  <h4>Sound/Audio</h4>
  <ul>
    <li>Sound must be user click-initiated with clear icon or appropriate text</li>
    <li>All sound must be muted/paused at start of animation.</li>
  </ul>
  <h4>Flash</h4>
  <p>Flash swf file export version 10 (or below) / Action Script 3.0 format (or earlier)</p>
  <ul>
    <li>24 FPS maximum (18 FPS in the US)</li>
    <li>Third party served Flash ads must be have a wmode set to "transparent" in their object/embed code.</li>
    <li>Third party served Flash ads using CSS style should not include "z-index:" parameter.</li>
    <li>All creatives must be designed with a solid background color, or 1 pixel border, to avoid unwanted color conflicts with the displaying page.</li>
    <li>All .swf files must be accompanied by .gif creative</li>
    <li>All .swf files must contain either of the following ActionScript code for a clickable button: 
      <ul>
        <li>ActionScript 2:<br />
          <code>on (release) {
          if (clickTag.substr(0,4) == "http") {
          getURL(_level0.clickTag, "_blank");
          }
        }</code></li>
        <li>ActionScript 3:<br />
          <code>clickBtn.addEventListener(MouseEvent.MOUSE_UP,  function(event: MouseEvent):void{<br />
            var sURL: String;<br />
            if ((sURL=root.loaderInfo.parameters.clickTAG)){<br />
            navigateToURL(new URLRequest(sURL), &quot;_blank&quot;);<br />
            }<br />
            }<br />
            );</code>
<br />
        </li>
      </ul>
    </li>
    <li>All Expandable Creative Must Be User-Initiated (Either Click-Initiated or Mouse-Over Initiated)</li>
  </ul>
  <h4>Rich Media</h4>
  <ul>
    <li>Full motion video must be user initiated </li>
    <li>Auto-play  video should be 15 seconds max in length</li>
    <li>All sound must be user initiated</li>
    <li>Roll over ads must have roll over hotspot of up to 1/8 size of the ad. Entire ad cannot be roll over.</li>
    <li>Must include clear CLOSE X button in at least 10 pt type (single "X" not acceptable)</li>
    <li>Mouse-Over Creative Must Retract On Mouse-Off</li>
    <li>Mouse-Over Expansion Should Include Language Specifying Functionality (e.g. Rollover To Learn More)</li>
    <li>Video ads must be third party served</li>
    <li>Expandable ads must be third party served by one of our our <a href="/resource.php?resource=questionnaire&amp;name=Expandable+Certified+Vendors">LinkedIn Certified Vendors</a>.</li>
  </ul>
  <p>For information on our certification process or to get certified, <a href="mailto:adcertification@linkedin.com?subject=Ad Certification">contact us today about Ad Certification.</a></p>
</div>
        <a href="/detailed-spec.php?spec=all_160x600&amp;name=all_160x600" class="more-less" id="all_160x600_toggle">details - 160x600</a> </div>
            <div class="spec">
        <h3>
          300x250        </h3>
        <div class="actions"><a href="/detailed-spec.php?spec=all_300x250&amp;name=all_300x250" class="btn-ternary">Detailed Spec</a> <a title="300x250" href="/assets/images/tn/300x250.jpg" class="thickbox btn-quaternary">View in Page</a> <a href="/detailed-spec.php?spec=all_300x250&amp;name=all_300x250&amp;print=true" class="print" title="Print">Print</a></div>
        <table>
  <caption>
  * border required only with white and transparent backgrounds<br>
  ** 30 seconds is the total maximum length of all animation, including all loops</caption>
  <tr>
    <th>Regions</th>
    <td>Global</td>
    <th>Dimensions</th>
    <td>300x250</td>
  </tr>
  <tr>
    <th><abbr title="Interactive Advertising Bureau">IAB</abbr> Name</th>
    <td>Medium Rectangle</td>
    <th>File Types</th>
    <td>GIF, JPG, PNG, SWF</td>
  </tr>
  <tr>
    <th>Size Limit</th>
    <td>40kb</td>
    <th>Border*</th>
    <td>1px*</td>
  </tr>
  <tr>
    <th>Rich Media Options</th>
    <td>Yes</td>
    <th>Animation Limit**</th>
    <td><p>15 sec for video quality autoplay<br />
    30 seconds otherwise**</p></td>
  </tr>
  <tr>
    <th>Video/Audio</th>
    <td>On user click</td>
    <th>3rd Party Tracking</th>
    <td>Yes</td>
  </tr>
  <tr>
    <th>Polite Download SWF Max</th>
    <td>100kb</td>
    <th>Polite Download Video Max</th>
    <td>2.2mb</td>
  </tr>
  <tr>
    <th>Ad Expand Direction &amp; Area</th>
    <td>Left - 600x250</td>
    <th></th>
    <td></td>
  </tr>
</table>
<div id="all_300x250_detail" class="spec-detail">
  <h4>Sound/Audio</h4>
  <ul>
    <li>Sound must be user click-initiated with clear icon or appropriate text</li>
    <li>All sound must be muted/paused at start of animation.</li>
  </ul>
  <h4>Flash</h4>
  <p>Flash swf file export version 10 (or below) / Action Script 3.0 format (or earlier)</p>
  <ul>
    <li>24 FPS maximum (18 FPS in the US)</li>
    <li>Third party served Flash ads must be have a wmode set to "transparent" in their object/embed code.</li>
    <li>Third party served Flash ads using CSS style should not include "z-index:" parameter.</li>
    <li>All creatives must be designed with a solid background color, or 1 pixel border, to avoid unwanted color conflicts with the displaying page.</li>
    <li>All .swf files must be accompanied by .gif creative</li>
    <li>All .swf files must contain the following ActionScript code for a clickable button:
      <ul>
        <li>ActionScript 2:<br />
          <code>on (release) {
            if (clickTag.substr(0,4) == &quot;http&quot;) {
            getURL(_level0.clickTag, &quot;_blank&quot;);
            }
            }</code></li>
        <li>ActionScript 3:<br />
          <code>clickBtn.addEventListener(MouseEvent.MOUSE_UP,  function(event: MouseEvent):void{<br />
            var sURL: String;<br />
            if ((sURL=root.loaderInfo.parameters.clickTAG)){<br />
            navigateToURL(new URLRequest(sURL), &quot;_blank&quot;);<br />
            }<br />
            }<br />
            );</code></li>
      </ul>
    </li>
    
    <li>All Expandable Creative Must Be User-Initiated (Either Click-Initiated or Mouse-Over Initiated)</li>
  </ul>
  <h4>Rich Media</h4>
  <ul>
    <li>Full motion video must be user initiated </li>
    <li>Auto-play  video should be 15 seconds max in length</li>
    <li>All sound must be user initiated</li>
    <li>Roll over ads must have roll over hotspot of up to 1/8 size of the ad. Entire ad cannot be roll over.</li>
    <li>Must include clear CLOSE X button in at least 10 pt type (single "X" not acceptable)</li>
    <li>Mouse-Over Creative Must Retract On Mouse-Off</li>
    <li>Mouse-Over Expansion Should Include Language Specifying Functionality (e.g. Rollover To Learn More)</li>
    <li>Video ads must be third party served</li>
    <li>Expandable ads must be third party served by one of our our <a href="/resource.php?resource=questionnaire&amp;name=Expandable+Certified+Vendors">LinkedIn Certified Vendors</a>.</li>
  </ul>
<p>For information on our certification process or to get certified, <a href="mailto:adcertification@linkedin.com?subject=Ad Certification">contact us today about Ad Certification.</a></p>
</div>
        <a href="/detailed-spec.php?spec=all_300x250&amp;name=all_300x250" class="more-less" id="all_300x250_toggle">details - 300x250</a> </div>
            <div class="spec">
        <h3>
          728x90        </h3>
        <div class="actions"><a href="/detailed-spec.php?spec=all_728x90&amp;name=all_728x90" class="btn-ternary">Detailed Spec</a> <a title="728x90" href="/assets/images/tn/728x90.jpg" class="thickbox btn-quaternary">View in Page</a> <a href="/detailed-spec.php?spec=all_728x90&amp;name=all_728x90&amp;print=true" class="print" title="Print">Print</a></div>
        <table>
  <caption>
  * border required only with white and transparent backgrounds<br>
  ** 30 seconds is the total maximum length of all animation, including all loops</caption>
  <tr>
    <th>Regions</th>
    <td>Global</td>
    <th>Dimensions</th>
    <td>728x90</td>
  </tr>
  <tr>
    <th><abbr title="Interactive Advertising Bureau">IAB</abbr> Name</th>
    <td>Leaderboard</td>
    <th>File Types</th>
    <td>GIF, JPG, PNG, SWF</td>
  </tr>
  <tr>
    <th>Size Limit</th>
    <td>40kb</td>
    <th>Border*</th>
    <td>1px*</td>
  </tr>
  <tr>
    <th>Rich Media Options</th>
    <td>Yes</td>
    <th>Animation Limit**</th>
    <td>15 sec for video quality autoplay<br />
    30 seconds otherwise**</td>
  </tr>
  <tr>
    <th>Video/Audio</th>
    <td>On user click</td>
    <th>3rd Party Tracking</th>
    <td>Yes</td>
  </tr>
  <tr>
    <th>Polite Download SWF Max</th>
    <td>100kb</td>
    <th>Polite Download Video Max</th>
    <td>2.2mb</td>
  </tr>
  <tr>
    <th>Ad Expand Direction &amp; Area</th>
    <td>Up - 728x310</td>
    <th></th>
    <td></td>
  </tr>
</table>
<div id="all_728x90_detail" class="spec-detail">
  <h4>Sound/Audio</h4>
  <ul>
    <li>Sound must be user click-initiated with clear icon or appropriate text</li>
    <li>All sound must be muted/paused at start of animation.</li>
  </ul>
  <h4>Flash</h4>
  <p>Flash swf file export version 10 (or below) / Action Script 3.0 format (or earlier)</p>
  <ul>
    <li>24 FPS maximum (18 FPS in the US)</li>
    <li>Third party served Flash ads must be have a wmode set to "transparent" in their object/embed code.</li>
    <li>Third party served Flash ads using CSS style should not include "z-index:" parameter.</li>
    <li>All creatives must be designed with a solid background color, or 1 pixel border, to avoid unwanted color conflicts with the displaying page.</li>
    <li>All .swf files must be accompanied by .gif creative</li>
    <li>All .swf files must contain the following ActionScript code for a clickable button:
      <ul>
        <li>ActionScript 2:<br />
          <code>on (release) {
            if (clickTag.substr(0,4) == &quot;http&quot;) {
            getURL(_level0.clickTag, &quot;_blank&quot;);
            }
            }</code></li>
        <li>ActionScript 3:<br />
          <code>clickBtn.addEventListener(MouseEvent.MOUSE_UP,  function(event: MouseEvent):void{<br />
            var sURL: String;<br />
            if ((sURL=root.loaderInfo.parameters.clickTAG)){<br />
            navigateToURL(new URLRequest(sURL), &quot;_blank&quot;);<br />
            }<br />
            }<br />
            );</code></li>
      </ul>
    </li>
    
    <li>All Expandable Creative Must Be User-Initiated (Either Click-Initiated or Mouse-Over Initiated)</li>
  </ul>
  <h4>Rich Media</h4>
  <ul>
    <li>Full motion video must be user initiated </li>
    <li>Auto-play  video should be 15 seconds max in length</li>
    <li>All sound must be user initiated</li>
    <li>Roll over ads must have roll over hotspot of up to 1/8 size of the ad. Entire ad cannot be roll over.</li>
    <li>Must include clear CLOSE X button in at least 10 pt type (single "X" not acceptable)</li>
    <li>Mouse-Over Creative Must Retract On Mouse-Off</li>
    <li>Mouse-Over Expansion Should Include Language Specifying Functionality (e.g. Rollover To Learn More)</li>
    <li>Video ads must be third party served</li>
    <li>Expandable ads must be third party served by one of our our <a href="/resource.php?resource=questionnaire&amp;name=Expandable+Certified+Vendors">LinkedIn Certified Vendors</a>.</li>
  </ul>
  <p>For information on our certification process or to get certified, <a href="mailto:adcertification@linkedin.com?subject=Ad Certification">contact us today about Ad Certification.</a></p>
</div>
        <a href="/detailed-spec.php?spec=all_728x90&amp;name=all_728x90" class="more-less" id="all_728x90_toggle">details - 728x90</a> </div>
            <div class="spec">
        <h3>
          textlink        </h3>
        <div class="actions"><a href="/detailed-spec.php?spec=all_textlink&amp;name=all_textlink" class="btn-ternary">Detailed Spec</a> <a title="textlink" href="/assets/images/tn/textlink.jpg" class="thickbox btn-quaternary">View in Page</a> <a href="/detailed-spec.php?spec=all_textlink&amp;name=all_textlink&amp;print=true" class="print" title="Print">Print</a></div>
         <table>
 <caption>* including spaces</caption>
  <tr>
    <th>Regions</th>
    <td>Global</td>
    <th>Dimensions</th>
    <td>960x17</td>
  </tr>
  <tr>
    <th><abbr title="Interactive Advertising Bureau">IAB</abbr> Name</th>
    <td>N/A</td>
    <th>Size Limit*</th>
    <td>90 characters*</td>
  </tr>
  <tr>
    <th>Rich Media Options</th>
    <td>No</td>
    <th>Video/Audio</th>
    <td>No</td>
  </tr>
  <tr>
    
    <th>3rd Party Tracking</th>
    <td>Yes</td>
    <th></th>
    <td></td>
  </tr>
</table>
<div id="all_textlink_detail" class="spec-detail">
<h4>Tips for writing text ads</h4>
 <p>LinkedIn is a professional site focused on making professionals more productive. We expect the tone and quality of text ads to be professional in nature. We reserve the right to refuse any text ad that does not meet our guidelines and best practices.  Do not reference specific brands, such as LinkedIn.</p>
 <!--p><a href="detailed-spec.php?spec=us_textlink&amp;name=us_textlink">View all ad guidelines and restrictions in the Detailed Spec &gt;&gt;</a></p-->
</div>
        <a href="/detailed-spec.php?spec=all_textlink&amp;name=all_textlink" class="more-less" id="all_textlink_toggle">details - textlink</a> </div>
          </div>
  </div>
  <div id="specs" class="extra panels">
  <div>
  <h2>Specifications</h2>
    <h3><a href="/">Common Specs</a></h3>
    <h3><a href="/category.php?category=Content+Ads">
    Content Ads    </a></h3>
    <h3><a href="/category.php?category=Sponsored+InMail">
    Sponsored InMail    </a></h3>
    <h3><a href="/category.php?category=Sponsored+Updates">
    Sponsored Updates    </a></h3>
    <h3><a href="/category.php?category=Social+Ads">
    Social Ads    </a></h3>
    <h3><a href="/category.php?category=Polls">
    Polls    </a></h3>
  </div>
</div>
<div id="resources" class="extra panels">
  <div>
  <h2>Resources</h2>
  <h3><a href="resource.php?resource=inmail_template&amp;name=Creative+Submission+Templates">Creative Submission Templates</a></h3>
  <h3><a href="/resource.php?resource=questionnaire&amp;name=Expandable+Certified+Vendors">Expandable Certified Vendors</a></h3>
  <h3><a href="resource.php?resource=terms&amp;name=Terms">Terms</a></h3>
  <!--h3><a href="resource.php?resource=contact&amp;name=Request+Ad+Certification">Request Ad Certification</a></h3-->
  <!--h3><a href="resource.php?resource=questionnaire&amp;name=Rich+Media+Certified+Vendors">Rich Media Certified Vendors</a></h3-->
</div>
</div>
<div id="links" class="extra panels">
  <div class="btn">
  <div><a href="http://marketing.linkedin.com/contact/?trk=en-all-site-li-mktag-site&amp;utm_source=adspecs&amp;utm_medium=adspecs&amp;utm_content=adspecs&amp;utm_campaign=adspecs" rel="external"><img src="/assets/images/btn_contactus.jpg" alt="Contact Us"/></a> <strong>Speak to our sales team</strong></div>
</div>
<div class="iab"> <a href="http://www.iab.net/iab_products_and_industry_services/508676/compliance/509534" rel="external">IAB Rich Media Creative Compliance</a> <a href="http://www.iab.net/iab_products_and_industry_services/508676/compliance/81617" rel="external">IAB Universal Ad Package Compliance</a> </div>
</div>
</div>
<!--script type="text/javascript" src="http://www.liasset.com/_util/tools/linkedin_footer.js.php?type=0&amp;style=0"></script-->

<script type="text/javascript" src="/assets/js/build/jquery.maskedinput-1.2.2.min.js"></script>
<script type="text/javascript" src="/assets/js/build/thickbox-compressed.js"></script> 
<script type="text/javascript">
	$(document).ready(function(){
		$('a[rel=external]').click(function() {
	window.open(this.href);
	return false;
});
$('a[rel=external_share]').click(function() {
	window.open(this.href,'','toolbar=0,status=0,width=626,height=436,scrollbars=yes');
	return false;
});		$('.auto_submit_form').change(function(event){
			if (jQuery(this).find("#form-name").length > 0) {
				document.getElementById('form-name').value = document.getElementById('form-spec').value;
			}
			this.submit();
   		});
 	});
   var _gaq = [['_setAccount', 'UA-20667913-3'], ['_trackPageview']];
   (function(d, t) {
    var g = d.createElement(t),
        s = d.getElementsByTagName(t)[0];
    g.async = true;
    g.src = ('https:' == location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    s.parentNode.insertBefore(g, s);
   })(document, 'script');
  </script><script type="text/javascript">
$(document).ready(function() {
		$('#index_detail').hide();        
        	$('#index_toggle').click(function() {
          	$('#index_detail').slideToggle("slow");
          	return false;
        });
				$('#all_160x600_detail').hide();        
        	$('#all_160x600_toggle').click(function() {
          	$('#all_160x600_detail').slideToggle("slow");
          	return false;
        });
				$('#all_300x250_detail').hide();        
        	$('#all_300x250_toggle').click(function() {
          	$('#all_300x250_detail').slideToggle("slow");
          	return false;
        });
				$('#all_728x90_detail').hide();        
        	$('#all_728x90_toggle').click(function() {
          	$('#all_728x90_detail').slideToggle("slow");
          	return false;
        });
				$('#all_textlink_detail').hide();        
        	$('#all_textlink_toggle').click(function() {
          	$('#all_textlink_detail').slideToggle("slow");
          	return false;
        });
	});
</script>
</body>
</html>
<!DOCTYPE html>
<html>
    <head>
        <title>Awio Web Services LLC</title>
        <meta name="description" content="Awio is a startup based in Pennsylvania, USA. We build services that help you do business online . attract new web traffic, track how it interacts with your website, and identify which of your ads lead to sales." />
        <link rel="stylesheet" type="text/css" href="bootstrap2.css" />
        <style type="text/css">
        
            #header {
                background: #eee url(grey.png);
                padding: 10px 0;
            }
            
            #nav {
                background: #06c url(blue.png) repeat-x;
                height: 40px;                
            }
            
            #nav ul {
                margin: 0;
                padding: 0;
                list-style: none;
                border-left: 1px solid #3366cc;
                overflow: auto;
            }
            
            #nav ul li {
                display: block;
                float: left;
                border-right: 1px solid #3366cc;
                padding: 11px 20px;
            }
            
            #nav ul li a:link, #nav ul li a:visited {
                color: #fff;
                font-weight: bold;
                font-size: 14px;
                text-transform: uppercase;
                text-shadow: #36c 1px 1px;
            }
            
            h3 {
                color: #aaa;
                margin: 30px 0 10px 0;
            }
            
            h4 {
                margin: 0 0 10px 0;
                padding-bottom: 1px;
                border-bottom: 2px solid #aaa;
            }
            
            p {
                /*
                background: #eee url(grey.png);
                border: 1px solid #eee;
                padding: 15px;
                -webkit-border-radius: 10px;
                -moz-border-radius: 10px;
                border-radius: 10px;
                font-weight: bold;
                */
                font-size: 14px;
                color: #444;
                line-height: 1.7em;
            }
           
            #improvely {
                background: url(improvely.png);
                border: 1px solid #ccc;
            }
 
            #w3counter {
                background: url(w3counter.png);
                border: 1px solid #ccc;                
            }
            
            #w3roi {
                background: url(w3roi.png);
                border: 1px solid #fff;
                color: #fff;
            }
            
            #dialshield {
                display: none;
                background: url(dialshield.png);
                border: 1px solid #fff;
                color: #fff;
            }
            
            #visitorboost {
                background: url(visitorboost.png);
                border: 1px solid #ccc;
            }
            
            #w3roi h1, #dialshield h1, #w3roi p, #dialshield p  {
                color: #fff;
            }
            
            #w3roi h1 a:link, #w3roi h1 a:visited, #dialshield h1 a:link, #dialshield h1 a:visited {
                color: #fff;
            }
            
            .product h1 a:link, .product h1 a:visited {
                text-decoration: none;
                color: #444;
            }
            
            .product {
                width: 940px;
                height: 250px;
                -webkit-border-radius: 10px;
                -moz-border-radius: 10px;
                border-radius: 10px;
                color: #444;
                margin-bottom: 30px;
                position: relative;
            }
            
            .product h1 {
                color: #444;
                margin: 28px 30px 0 480px;
                padding: 0;
                font-weight: normal;
                font-size: 24px;
            }
            
            .product p {
                margin: 10px 30px 0 480px;
                padding: 0;
                line-height: 2em;
                font-size: 14px;
                color: #444;
            }
            
            .product a.btn {
                position: absolute;
                left: 480px;
                bottom: 17px;
            }
            
            .ads {
                margin-top: 10px;
                font-size: 14px;
                line-height: 1.5em;
            }
            
            #footer {
                margin-top: 30px;
                background: #06c url(blue.png) repeat-x;
                color: #fff;
                padding: 11px 0;
                font-size: 12px;
            }
            
            #footer img {
                margin-left: 5px;
                position: relative;
                top: 2px;
            }
            
            #cctip {
                float: right;
                background: #fff;
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 10px;
                margin-top: 5px;
                color: #444;
            }
            
        </style>
    </head>
    <body>
        
        <div id="header">
            <div class="container">
                <div id="cctip">
                    Here because of a charge on your credit card? <a href="#contact">Click here</a>.
                </div>
                <a href="/"><img src="logo.png" alt="Awio Web Services LLC" /></a>
            </div>
        </div>
        
        <div id="nav">
            <div class="container">
                <ul>
                    <li><a href="#top">About Us</a></li>
                    <li><a href="#products">Our Products</a></li>
                    <li><a href="#advertising">Advertising</a></li>
                    <li><a href="#contact">Contact Us</a></li>
                </ul>
            </div>
        </div>
        
        <div id="body">
            <div class="container">
                
                <a name="top"></a>
                <h3>About Us</h3>
                
                <p style="font-size: 18px">
                    Awio is a startup based in Pennsylvania, USA. We build services that help you do business online &mdash;
                    attract new web traffic, track how it interacts with your website, and identify which of your ads lead
                    to sales.
                </p>
                                
                <a name="products"></a>
                <h3>Our Products</h3>

                <div class="product" id="improvely">
                    <h1><a href="http://www.improvely.com">Improvely</a></h1>
                    <p>Improvely combines click and conversion tracking, click fraud detection, A/B split testing for landing 
                    pages, and affiliate marketing tools into one easy-to-use platform. </p>
                    <a class="btn" href="http://www.improvely.com"><i class="icon share"></i> Visit the Improvely Website</a>
                </div>
                 
                <div class="product" id="dialshield">
                    <h1><a href="http://www.dialshield.com">DialShield</a></h1>
                    <p>Reduce spam and payment fraud by adding real-time phone verification to your website forms. DialShield
                    provides an API for automatically calling and texting phones from your website.</p>
                    <a class="btn" href="http://www.dialshield.com"><i class="icon share"></i> Visit the DialShield Website</a>
                </div>

                <div class="product" id="w3counter">
                    <h1><a href="http://www.w3counter.com">W3Counter</a></h1>
                    <p>W3Counter is your free, hosted, easy-to-use website analytics solution for answering the key questions
                    about your website: who's your audience, how they find your site, and what interests them.</p>
                    <a class="btn" href="http://www.w3counter.com"><i class="icon share"></i> Visit the W3Counter Website</a>
                </div>

                <!--
                <div class="product" id="w3roi">
                    <h1><a href="http://www.w3roi.com">W3ROI</a></h1>
                    <p>Measure and optimize the performance of your online advertising &mdash; track the clicks, leads and
                    sales from all your avertising efforts in one place.</p>
                    <a class="btn" href="http://www.w3roi.com"><i class="icon share"></i> Visit the W3ROI Website</a>
                </div>
                -->
                
                <div class="product" id="visitorboost">
                    <h1><a href="http://www.visitorboost.com">VisitorBoost</a></h1>
                    <p>Affordable full-screen popunder advertising packages through our ad network partner. Guaranteed
                    traffic within 1-2 business days with geographic and interest targeting.</p>
                    <a class="btn" href="http://www.visitorboost.com"><i class="icon share"></i> Visit the VisitorBoost Website</a>
                </div>
                
                <a name="advertising"></a>
                <h3>Advertising</h3>
                
                <p>Advertising space is occasionally available on some of our websites. Current placements available:</p>
                
                <div class="row ads">
                    <div class="span4 offset2">
                        <a href="http://buysellads.com/buy/detail/99" style="font-weight: bold">W3Counter.com Stats Header</a><br />
                        468 x 60 <span style="color: #666">Top Right, Image-Only Ad</span>
                    </div>
                    
                    <div class="span4">
                        <a href="http://buysellads.com/buy/detail/99" style="font-weight: bold">W3Counter.com Stats Sidebar</a><br />
                        125 x 125 <span style="color: #666">Middle Right, Image-Only Ad</span>
                    </div>
                </div>
                
                <div class="clear"></div>
                
                <a name="contact"></a>
                <h3>Contact Us</h3>
                
                <p>Payments made at any of our websites will appear on your billing statement under the name of our company,
                not the individual domain you purchased at. You may have made a purchase at <a href="http://www.improvely.com">Improvely</a>, 
                <a href="http://www.visitorboost.com">VisitorBoost</a>, <a href="http://www.w3roi.com/login">W3ROI</a> or 
                <a href="http://www.w3counter.com">W3Counter</a>.</p>
                
                <p>If you don't recall making a purchase at any of those sites, ask the coworkers or family that might have
                access to your credit card. If you still don't think you made a purchase, e-mail us and we'll take care of
                you right away.</p>

                <div class="row" style="margin-top: 20px">
                    
                    <div class="span3">
                        <h4>E-mail</h4>
                        <a href="mailto:dan@awio.com">dan@awio.com</a>
                    </div>
                    <div class="span3">
                        <h4>Postal Mail</h4>
                        Awio Web Services LLC<br />
                        219 Chatham Pl<br />
                        Lansdale, PA 19446
                    </div>
                    <div class="span3">
                        <h4>Voice Mail &amp; Fax</h4>
                        (888) 304-5864
                    </div>
                    <div class="span3">
                        <h4>Help Desk</h4>
                        <a href="http://awio.zendesk.com">http://awio.zendesk.com</a>
                    </div>
                    
                </div>
                <div class="clear"></div>
                
            </div>
        </div>
        
        <div id="footer">
            <div class="container">
                <div style="float: right"> 
					<!-- Begin W3Counter Tracking Code --> 
					<script type="text/javascript" src="http://www.w3counter.com/tracker.js"></script> 
					<script type="text/javascript"> 
					w3counter(4754);
					</script> 
					<noscript> 
					<div><a href="http://www.w3counter.com"><img src="http://www.w3counter.com/tracker.php?id=4754" style="border: 0" alt="W3Counter Web Stats" /></a></div> 
					</noscript> 
					<!-- End W3Counter Tracking Code-->                     
                </div>
                <div style="float: right; font-weight: bold">web stats by</div>
                Copyright &copy; 2004-2014 Awio Web Services LLC. All rights reserved.
            </div>
        </div>
        
    </body>
</html>

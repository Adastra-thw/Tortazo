<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>
      W3Counter: Free Web Analytics and Visit Counter          </title>

    <!-- Bootstrap core CSS -->
    <link href="/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">
    <link href="/css/2014-website.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

    <script src="https://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="https://code.jquery.com/ui/1.10.4/jquery-ui.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>

    
    <link href='http://fonts.googleapis.com/css?family=Droid+Sans:400,700' rel='stylesheet' type='text/css'>

    <script type="text/javascript">
    var im_domain = 'awio';
    var im_project_id = 2;
    (function(e,t){window._improvely=[];var n=e.getElementsByTagName("script")[0];var r=e.createElement("script");r.type="text/javascript";r.src="https://"+im_domain+".iljmp.com/improvely.js";r.async=true;n.parentNode.insertBefore(r,n);if(typeof t.init=="undefined"){t.init=function(e,t){window._improvely.push(["init",e,t])};t.goal=function(e){window._improvely.push(["goal",e])};t.label=function(e){window._improvely.push(["label",e])}}window.improvely=t;t.init(im_domain,im_project_id)})(document,window.improvely||[])
    </script>
    <meta name="google-site-verification" content="0ZPavT651boyurYXRIqXuWxiVPbA9JxO4cj1mFFJu2Q" />  

  </head>

  <body id="body">
    <div id="wrap">

      <div class="navbar navbar-default navbar-static-top" role="navigation">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
              <span class="sr-only">Navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/"><img style="height: 40px" src="/images/logo_transparent.png" /></a>
          </div>
          <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav navbar-right">
              <li><a href="/globalstats.php">Global Market Share</a></li>
              <li class="active"><a href="/signup">Free Signup</a></li>
              <li><a href="/stats">Log In</a></li>
            </ul>
          </div>
        </div>
      </div>
        
      <div class="container-fluid main">
    <div class="row">
        <div class="col-md-5 col-lg-4 col-xs-12">

          <div style="padding: 0 30px; font-size: 20px" class="intro">

            <h1 style="margin: 40px 0 0 0; font-size: 36px; line-height: 1.3em; font-weight: bold">Free Web Stats</h1>
            <h2 style="margin: 0 0 40px 0; font-size: 24px; font-weight: bold">For Your Website or Blog</h2>

            <p style="margin-bottom: 40px; line-height: 1.8em">
              Add our free counter or badge to your site and learn all about your website visitors &mdash;
              where they come from, how they use your site and which pages they love.
            </p>

            <div style="font-size: 18px; padding-bottom: 20px">
              <a href="/signup" class="btn btn-success">Sign Up For Free</a> 
              <span style="position: relative; top: 5px">&nbsp; or &nbsp;</span>
              <a href="/stats/pulse/1" class="btn btn-default">Try It Out</a> 
            </div>

          </div>

        </div>
        <div class="col-md-7 col-lg-8 hidden-sm hidden-xs" id="hero">

        </div>
      
    </div>

    <div class="row" style="background: #c1deef">
      <div class="col-md-4 col-xs-12">
        <div class="featurebox">
          <h3>Free Web Stats</h3>
          <p>
            For websites with less than 5000 page views per day, get free web stats reports for life. 
            Not a free trial, no credit card required.
          </p>
          <i class="fa fa-caret-down"></i>
        </div>
      </div>
      <div class="col-md-4 col-xs-12">
        <div class="featurebox">
          <h3>Customizable Visit Counter</h3>
          <p>
            Choose from nearly 100 counter styles, from simple badges to real-time visitor counts on your site.
            Find the perfect design for you.
          </p>
          <i class="fa fa-caret-down"></i>
        </div>
      </div>
      <div class="col-md-4 col-xs-12">
        <div class="featurebox">
          <h3>Real-Time Reports</h3>
          <p>
            W3Counter offers over 20 real-time web stats reports. We're always up-to-date, updating with each 
            new visitor to your website.
          </p>
          <i class="fa fa-caret-down"></i>
        </div>
      </div>
    </div>

    <div class="row" style="overflow: auto">
      <div class="col-md-7 col-xs-12">

        <h3 style="margin: 40px 0 20px 20px; font-size: 24px">What's Happening Now</h3>

        <div id="activity">
          <table class="table table-responsive">
            <tbody></tbody>
          </table>
        </div>

      </div>
      <div class="col-md-5 col-xs-12">

        <div class="featurebox" style="margin-bottom: 0">
          <h4>Analytics for Marketers</h4>
          <p>
            Looking for conversion tracking, PPC click fraud monitoring and revenue tracking? 
            You'll love our service for e-commerce and business sites, <a href="https://www.improvely.com">Improvely</a>.
          </p>
        </div>

        <div class="featurebox" style="margin-top: 20px; margin-bottom: 40px">
          <h4>Advertise on W3Counter</h4>
          <p>
            W3Counter's free service is supported by several non-intrusive banner ads on our 
            reports. Reach tens of thousands of site owners by 
            <a href="http://buysellads.com/buy/detail/99" rel="nofollow">advertising here</a>.
          </p>
        </div>
      </div>
    </div>
</div>

<script type="text/javascript">
  var last_activity = {};
  var activity_count = 0;

  function updateActivity() {
    if (activity_count == 0) {
      activity_count = 8;
    } else {
      activity_count = 1;
    }
    $.ajax({ 
      method: 'get',
      url: '/activity?count=' + activity_count,
      dataType: 'json',
      success: function(data) {
        if (data != null && data.length) {
          for (var i = 0; i < data.length; i++) { 
            renderActivity(data[i]);
          }
        }
      }
    });
  }

  function renderActivity(item){
    if (item.ip == last_activity.ip) 
      return;
        
    var d = new Date(item.timestamp * 1000);
    var hours = d.getHours();
    var minutes = d.getMinutes();
    var ampm = 'AM';
    
    if (hours == 12) {
      ampm = 'PM';
    } else if (hours > 12) {
      ampm = 'PM';
      hours -= 12;
    } else if (hours == 0) {
      hours = 12;
    }

    if (minutes < 10) {
      minutes = '0' + minutes;
    }
    
    var time = hours + ':' + minutes + ' ' + ampm;

    html = '<tr>';
    html += '<td class="icon" style="padding-right: 0"><img src="/images/icons/flags/' + item.countryCode + '.gif" alt="' + item.countryCode + ' Flag" style="padding-top: 13px; padding-bottom: 12px" /></td>';
    html += '<td class="icon"><img src="/images/icons/browser_' + item.browserFamily + '.gif" alt="' + item.browserFaily + '" /></td>';
    html += '<td class="icon" style="padding-left: 0"><img src="/images/icons/' + item.os + '.gif" /></td>';
    html += '<td class="time">' + time + '</td>';
    html += '<td class="visit">';
    html += 'New visit to ' + item.webpageName;
    html += '</td>';
    html += '</tr>';

    var existing = $('#activity table tbody').html();
    $('#activity table tbody').html(html + existing);
    
    last_activity = item;
  }
   
  $(function() {
      setInterval(updateActivity, 5000);
      updateActivity();
  });
</script>

    </div><!-- //wrap -->
    <div id="footer">
      Copyright &copy; 2004-2014 &nbsp;<a href="http://www.awio.com">Awio Web Services LLC</a>
      &nbsp;&middot;&nbsp;
      <a href="mailto:admin@w3counter.com">Contact</a>
      &nbsp;&middot;&nbsp;
      <a href="/legal/terms">Terms of Service</a>
      &nbsp;&middot;&nbsp;
      <a href="/legal/privacy">Privacy Policy</a>

      <!-- Quantcast Tag -->
      <script type="text/javascript">
      var _qevents = _qevents || [];

      (function() {
      var elem = document.createElement('script');
      elem.src = (document.location.protocol == "https:" ? "https://secure" : "http://edge") + ".quantserve.com/quant.js";
      elem.async = true;
      elem.type = "text/javascript";
      var scpt = document.getElementsByTagName('script')[0];
      scpt.parentNode.insertBefore(elem, scpt);
      })();

      _qevents.push({
      qacct:"p-bdUJejYHg9Ff-"
      });
      </script>

      <noscript>
      <div style="display:none;">
      <img src="//pixel.quantserve.com/pixel/p-bdUJejYHg9Ff-.gif" border="0" height="1" width="1" alt="Quantcast"/>
      </div>
      </noscript>
      <!-- End Quantcast tag -->

      <!-- Begin W3Counter Secure Tracking Code -->
      <script type="text/javascript" src="https://www.w3counter.com/securetracker.js"></script>
      <script type="text/javascript">
      w3counter(1);
      </script>
      <noscript>
      <div><a href="http://www.w3counter.com"><img src="https://www.w3counter.com/tracker.php?id=1" style="border: 0" alt="W3Counter" /></a></div>
      </noscript>
      <!-- End W3Counter Secure Tracking Code-->

      <!-- Begin W3Counter Pulse Real-Time Heartbeat Code -->
      <script type="text/javascript">
      (function(){
        var ps = document.createElement('script');
         ps.type = 'text/javascript';
         ps.async = true;
         ps.src = '//pulse.w3counter.com/pulse.js?id=1';
        (document.getElementsByTagName('head')[0]||document.getElementsByTagName('body')[0]).appendChild(ps);
      })();
      </script>
      <!-- End W3Counter Pulse Real-Time Heartbeat Code-->

      <script type="text/javascript">
      Shopify = { shop: 'www.w3counter.com' };
      </script>
      <script type="text/javascript" src="https://icf.improvely.com/icf-button.js?shop=www.w3counter.com"></script>

    </div>
  </body>
</html>

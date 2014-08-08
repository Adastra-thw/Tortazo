<?php
# Front page - news, latests projects, etc.
# Copyright 1999-2000 (c) The SourceForge Crew
# Copyright 2003-2006 (c) Mathieu Roy <yeupou--gnu.org>
# Copyright (C) 2006, 2007  Sylvain Beucler
#
# This file is part of Savane.
# 
# Savane is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# Savane is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

require_once('../include/init.php');
require_once('../include/account.php');
require_once('../include/sane.php');

Header("Expires: Wed, 11 Nov 1998 11:11:11 GMT");
Header("Cache-Control: no-cache");
Header("Cache-Control: must-revalidate");

extract(sane_import('request', array('from_brother')));

# Block here potential robots
# 2006-12-04, yeupou: allows them to login, so they can post on trackers of
# their projects. This is a compromise between the need to avoid spam by all
# means and the fact that we still want to allow to work people in obvious
# legit cases even if they are blacklisted.
# They wont be able to use savane normally but only to post on the project
# they are member of. The way to go for them is to ask their IP to be delisted,
# not from us to maintain another list of exceptions. If they cant, it is sad
# but we cannot encourage this because it would defeat the whole purpose of
# DNSbl, while DNSbl seems to be the only truly effective way to get rid of
# spams.
#dnsbl_check();

# Logged users have no business here
if (user_isloggedin() && !$from_brother)
{ session_redirect($GLOBALS['sys_home']."my/"); }

# Input checks
extract(sane_import('request',
  array('form_loginname', 'form_pw', 'cookie_for_a_year',
	'stay_in_ssl', 'brotherhood',
	'uri', 'login', 'cookie_test')));

#if (isset($GLOBALS['sys_https_host']) && !session_issecure())
#{
#  # Force use of TLS for login
#  header('Location: '.$GLOBALS['sys_https_url'].$_SERVER['REQUEST_URI']);
#}

# Check cookie support
if (!$from_brother and !isset($_COOKIE["cookie_probe"]))
{
  if (!$cookie_test)
    {
    // Attempt to set a cookie to go to a new page to see if the client will indeed send that cookie.
    session_cookie('cookie_probe', 1);
    // $uri used to be not url-encoded, it caused login problems,
    // see sr#108277 (https://savannah.gnu.org/support/?108277)
    header('Location: login.php?uri='.urlencode($uri).'&cookie_test=1');
    }
  else # 
    {
      fb(sprintf(_("Savane thinks your cookies are not activated for %s. To log-in, we need you to activate cookies in your web browser for this website. Please do so and click here:"), $sys_default_domain).' '.$GLOBALS['sys_https_url'].$GLOBALS['sys_home'].'account/login.php?uri='.$uri, 1);
    }
}

if (!empty($login))
{
  if ($from_brother) 
  {
    extract(sane_import('get', array('session_uid', 'session_hash')));
    if (!ctype_digit($session_uid))
      { exit("Invalid session_uid"); }
    if (!ctype_alnum($session_hash))
      { exit("Invalid session_hash"); }
  }

  if (isset($session_uid) and session_exists($session_uid, $session_hash)) 
  {
    $GLOBALS['session_hash'] = $session_hash;
    session_set_new_cookies($session_uid, $cookie_for_a_year, $stay_in_ssl);
    $success = 1;
  } 
  else 
  {
    $success = session_login_valid($form_loginname, $form_pw, 0, $cookie_for_a_year, 0, $stay_in_ssl);
  }

  if ($success)
    {
      # Set up the theme, if the user has selected any in the user
      # preferences -- but give priority to a cookie, if set.
      if (!isset($_COOKIE['SV_THEME']))
        {
          $theme_result = user_get_result_set(user_getid());
          $theme = db_result($theme_result, 0, 'theme');
          if (strlen($theme) > 0)
            {
              setcookie('SV_THEME', $theme, time() + 60*60*24,
                $GLOBALS['sys_home'], $GLOBALS['sys_default_domain']);
            }
	}


      # We return to our brother 'my', where we login originally,
      # unless we are request to go to an uri
      if (!$uri)
	{
	  $uri = $GLOBALS['sys_home'] . 'my/';
	}
      
      # If a brother server exists, login there too, if we are not
      # already coming from there
      if (!empty($GLOBALS['sys_brother_domain']) && $brotherhood)
	{
	  if (session_issecure())
	    { $http = "https"; }
	  else
	    { $http = "http"; }

	  if (!$from_brother)
	    {
	      # Go there saying hello to your brother
	      header ("Location: ".$http."://".$GLOBALS['sys_brother_domain'].$GLOBALS['sys_home']."/account/login.php?session_uid=".user_getid()."&session_hash=".$GLOBALS['session_hash']."&cookie_for_a_year=$cookie_for_a_year&from_brother=1&login=1&stay_in_ssl=$stay_in_ssl&brotherhood=1&uri=".urlencode($uri));
	      exit;
	    }
	  else
	    {
	      header("Location: ".$http."://".$GLOBALS['sys_brother_domain'].$uri);
	      exit;
	    }
	}
      else
	{
	  # If No brother server exists, just go to 'my' page 
          # unless we are request to go to an uri

	  // Optionally stay in TLS mode
	  if ($stay_in_ssl)
	    {
	      // switch to requested HTTPs mode
	      header("Location: {$GLOBALS['sys_https_url']}$uri");
	    }
	  else
	    {
	      // Stay in current http mode (also avoids mentioning
	      // hostname&port, which can be useful in test
	      // environments with port forwarding)
	      header("Location: $uri");
	    }
	  exit;
	}

    }
}

if (isset($session_hash))
{
   # Nuke their old session securely. 
   session_delete_cookie('session_hash');
   db_execute("DELETE FROM session WHERE session_hash=? AND user=?",
	      array($session_hash, $user_id));
}


site_header(array('title'=>_("Login")));

if (!empty($login) && !$success)
{

  if ("Account Pending" == $feedback)
    {

      print '<h3>'._("Pending Account").'</h3>';
      print '<p>'._("Your account is currently pending your email confirmation. Visiting the link sent to you in this email will activate your account.").'</p>';
      print '<p>'._("If you need this email resent, please click below and a confirmation email will be sent to the email address you provided in registration.").'</p>';
      print '<p><a href="pending-resend.php?form_user='.htmlspecialchars($form_loginname, ENT_QUOTES).'">['._("Resend Confirmation Email").']</a></p>';

    }
  else
    {
      # print helpful error message
      print '<div class="splitright"><div class="boxitem">';
      print '<div class="warn">'._("Troubleshooting:").'</div></div><ul class="boxli">'.
	'<li class="boxitemalt">'._("Is the \"Caps Lock\" or \"A\" light on your keyboard on?").'<br />'._("If so, hit \"Caps Lock\" key before trying again.").'</li>'.
	'<li class="boxitem">'._("Did you forget or misspell your password?").'<br />'.utils_link('lostpw.php', _("You can recover your password using the lost password form.")).'</li>'.
	'<li class="boxitemalt">'._("Still having trouble?").'<br />'.utils_link($GLOBALS['sys_home'].'support/?group='.$GLOBALS['sys_unix_group_name'],  _("Fill a support request.")).'</li>';
      print '</ul></div>';
    }

}

if (isset($GLOBALS['sys_https_host']))
{
  utils_get_content("account/login");
}
print '<form action="'.$GLOBALS['sys_https_url'].$GLOBALS['sys_home'].'account/login.php" method="post">';
print '<input type="hidden" name="uri" value="'.htmlspecialchars($uri, ENT_QUOTES).'" />';

# Shortcuts to New Account and Lost Password have a tabindex superior to 
# the rest of form, 
# so they dont mess with the normal order when you press TAB on the keyboard
# (login -> password -> post)
print '<p><span class="preinput">'._("Login Name:").'</span><br />&nbsp;&nbsp;';
print '<input type="text" name="form_loginname" value="'.htmlspecialchars($form_loginname, ENT_QUOTES).'" tabindex="1" /> <a class="smaller" href="register.php" tabindex="2">['._("No account yet?").']</a></p>';

print '<p><span class="preinput">'._("Password:").'</span><br />&nbsp;&nbsp;';
print '<input type="password" name="form_pw" tabindex="1" /> <a class="smaller" href="lostpw.php" tabindex="2">['._("Lost your password?").']</a></p>';

if (isset($GLOBALS['sys_https_host']))
{

  $checked = 'checked="checked" ';
  if ($login and !$stay_in_ssl)
    { $checked = ''; }

  print '<p><input type="checkbox" name="stay_in_ssl" value="1" tabindex="1" '.$checked.'/><span class="preinput">';
  print _("Stay in secure (https) mode after login")."</span><br />\n";
}
else
{
  print '<p class="warn"><input type="hidden" name="stay_in_ssl" value="0" />';
  print _("This server does not encrypt data (no https), so the password you sent may be viewed by other people. Do not use any important passwords.").'</p>';
}

$checked = '';
if ($cookie_for_a_year)
  { $checked = 'checked="checked" '; }

print '<p><input type="checkbox" name="cookie_for_a_year" tabindex="1" value="1" '.$checked.'/><span class="preinput">'._("Remember me").'</span><br />';
print '<span class="text">'._("For a year, your login information will be stored in a cookie. Use this only if you are using your own computer.").'</span>';

if (!empty($GLOBALS['sys_brother_domain']))
{
  $checked = 'checked="checked" ';
  if ($login and !$brotherhood)
     $checked = '';

  print '<p><input type="checkbox" name="brotherhood" value="1" tabindex="1" '.$checked.'/><span class="preinput">';
  printf (_("Login also in %s").'</span><br />', $GLOBALS['sys_brother_domain']);
}

print '<div class="center"><input type="submit" name="login" value="'._("Login").'" tabindex="1" /></div>';
print '</form>';

$HTML->footer(array());

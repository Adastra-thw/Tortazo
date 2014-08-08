<?php
# Resend the confirmation hash to a pending (not yet validated) user
# 
# Copyright 1999-2000 (c) The SourceForge Crew
# Copyright (C) 2007  Sylvain Beucler
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
# Copyright 1999-2000 (c) The SourceForge Crew

require_once('../include/init.php');
require_once('../include/database.php');
require_once('../include/dnsbl.php');
require_once('../include/spam.php');
require_once('../include/sane.php');
require_once('../include/sendmail.php');


# Block here potential robots
dnsbl_check();
# Block banned IP
spam_bancheck();

extract(sane_import('get', array('form_user')));

$res_user = db_execute("SELECT * FROM user WHERE user_name=?", array($form_user));
$row_user = db_fetch_array($res_user);

# only mail if pending
if ($row_user['status'] == 'P') {

  # send mail
  $message = sprintf(_("Thank you for registering on the %s web site."),$GLOBALS['sys_name'])."\n"
    . _("In order to complete your registration, visit the following url:")."\n\n"
    . $GLOBALS['sys_https_url'].$GLOBALS['sys_home']."account/verify.php?confirm_hash=$row_user[confirm_hash]\n\n"
    . _("Enjoy the site").".\n\n"
    . sprintf(_("-- the %s team."),$GLOBALS['sys_name'])."\n";
	
	
  sendmail_mail($GLOBALS['sys_mail_replyto'] . "@".$GLOBALS['sys_mail_domain'],
		$row_user['email'],
		$GLOBALS['sys_name'] . " " . _("Account Registration"),
		$message);

  $HTML->header(array('title'=>_("Account Pending Verification")));

  print '<h3>'._("Pending Account").'</h3>';
  print '<p>'._("Your email confirmation has been resent. Visit the link in this email to complete the registration process.").'</p>';
  print '<p><a href="'.$GLOBALS['sys_home'].'">['._("Return to Home Page").']</a></p>';
 
} else {
  exit_error(_("Error"),_("This account is not pending verification."));
}

$HTML->footer(array());

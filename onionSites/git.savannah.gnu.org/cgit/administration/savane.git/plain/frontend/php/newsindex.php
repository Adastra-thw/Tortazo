<?php
# Copyright 1999-2000 (c) The SourceForge Crew
# Copyright 2002-2006 (c) Mathieu Roy <yeupou--gnu.org>
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

require_once('../include/init.php');
require_once('../include/news/general.php');


if (!$group_id) 
{
  $group_id = $GLOBALS['sys_group_id'];
}

extract(sane_import('request', array('feedback', 'limit')));


if (isset($limit))
     $limit = intval($limit);
else
     $limit = 10;

$project=project_get_object($group_id);
if (!$project->Uses("news"))
{ exit_error(_("This project has turned off the news tool.")); }
 
site_project_header(array('group'=>$group_id,
			  'context'=>'news'));


/* permit to the user to specify something */

$form_opening = '<form action="'. $_SERVER['PHP_SELF'] .'#options" method="get">';
# I18N
# %s is an input field
$form = sprintf(_("Print summaries for the %s latest news."), '<input type="text" name="limit" size="4" value="'.$limit.'" />');
if (isset($group))
{ $form .= '<input type="hidden" name="group" value="'.$group.'" />'; }
$form_submit = '<input class="bold" type="submit" value="'._("Apply").'"  />';

print html_show_displayoptions($form, $form_opening, $form_submit);

print "<br />\n";

print $HTML->box_top(_("Latest News Approved - With Summaries"));
print news_show_latest($group_id, $limit, "true", $start_from="nolinks");
print $HTML->box_bottom();

/* A box with no summaries, if they are not all already shown */
if ($limit < news_total_number($group_id)) 
{
  print "<br />\n";
  print $HTML->box_top(_("Older News Approved"));
  print news_show_latest($group_id, 0, "false", $start_from=$limit);
  print $HTML->box_bottom();
}

site_project_footer(array());

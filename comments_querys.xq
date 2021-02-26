module namespace c = "FiveDayForecast_testesapenas.functions";

declare updating function c:new_comment($name,$comment,$date,$location_id) {
  for $a in collection('FiveDayForecast_testesapenas')//weatherdata
  let $b := $a/location/location
  let $c := $a//comment 
  where $b/@geobaseid = $location_id
  return insert nodes (
    <comment>
      <id>{max($c/id)+1}</id>
      <name>{$name}</name>
      <text>{$comment}</text>
      <date>{$date}</date>
    </comment> 
  ) as first into $a/location 
};

declare function c:new_id($name,$comment,$date,$location_id) as element()* {
for $a in collection('FiveDayForecast_testesapenas')//weatherdata
let $b := $a/location/location
let $c := $a//comment
where $b/@geobaseid = $location_id
return(
  max($c/id)+1
)
};

declare updating function c:edit_comment($comment,$location_id, $id) {
  for $a in collection('FiveDayForecast_testesapenas')//weatherdata/location
  let $b := $a/location
  where $b/@geobaseid = $location_id 
  for $d in $a//comment
  where $d/id = $id
  return replace node $d/text/text() with $comment
};

declare updating function c:remove_comment($location_id, $id) {
  for $a in collection('FiveDayForecast_testesapenas')//weatherdata/location
  let $b := $a/location
  where $b/@geobaseid = $location_id
  for $d in $a//comment
  where $d/id = $id
  return delete node $d
};

declare function c:list_comments($location_id) as element()* {
  for $a in collection('FiveDayForecast_testesapenas')//weatherdata/location
  let $b := $a/location
  where $b/@geobaseid = $location_id
  let $c := $a//comment
  return 
    <comments>
      {$c}
    </comments>
};
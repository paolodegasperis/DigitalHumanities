<?php

function updateRSSFeed() {
    $rssUrl = "https://www.ansa.it/canale_tecnologia/notizie/tecnologia_rss.xml";
    $xml = simplexml_load_file($rssUrl);

    $htmlContent = '<html><head><title>Feed RSS ANSA Tecnologia</title></head><body>';
    $htmlContent .= '<h1>Articoli ANSA Tecnologia</h1>';

    foreach ($xml->channel->item as $item) {
        $title = $item->title;
        $link = $item->link;
        $description = $item->description;

        $htmlContent .= "<h2>$title</h2>";
        $htmlContent .= "<p>$description</p>";
        $htmlContent .= "<a href='$link'>Leggi di più</a><br><br>";
    }

    $htmlContent .= '</body></html>';
    file_put_contents('ansa_feed.html', $htmlContent);
}

updateRSSFeed();

?>


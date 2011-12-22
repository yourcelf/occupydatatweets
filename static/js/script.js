// Utility
var HTML_CHARS = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
    '`': '&#x60;'
};
var _htmlReplacer = function (match) {
    return HTML_CHARS[match];
};

var escapeHTML = function (string) {
    if (string === null || typeof string === "undefined") {
        string = "";
    } else {
        string = String(string);
    }
    return string.replace(/[&<>"'\/`]/g, _htmlReplacer);
};

// Pages
var tweet_link_counts = function (data) {
    var categories = {};
    for (var i = 0; i < data.results.length; i++) {
        var result = data.results[i];
        var domain_parts = result.url.split("//");
        var url_display;
        categories[result.category] = 1;
        if (domain_parts.length > 1) {
            url_display = domain_parts[1].replace(/^www\./, "").substring(0, 15) + "...";
        } else {
            url_display = domain_parts[0].substring(0, 15) + "...";
        }
        var href;
        if (result.url.substring(0, 4) == "http") {
            href = result.url.replace("'", "\\'");
        } else {
            href = "javascript:void(0)";
        }
        $("#tweets").append(
                

            $("<div class='tweet-link " + result.category + " " + result.subcategory + "'/>").html(
                "<span class='count' title='Total number of tweets: " + result.tweet_count + "'>" + result.tweet_count + "</span>" +
                "<a href='" + href + "' rel='nofollow'" + 
                " title='" + escapeHTML(result.category + " " + 
                                        result.subcategory + 
                                        "; link first appeared " + result.first_appearance) + "'" +
                ">" + escapeHTML(url_display) + "</a>"
            )
        );
    }

    // Categories
    for (var category in categories) {
        (function(category) {
            var link = $("<a href='#'/>").html(category).click(function() {
                $(".muted").removeClass("muted");
                if ($(this).parent(".category").hasClass("showing")) {
                    $(this).parent(".category").removeClass("showing");
                } else {
                    $(".showing").removeClass("showing");
                    $(this).parent(".category").addClass("showing");
                    $(".category:not(.showing").addClass("muted");
                    $(".tweet-link:not(." + category + ")").addClass("muted");

                }
                return false;
            });
            var div = $("<div class='category'/>");
            div.append("<span class='swatch " + category + "'></span>");
            div.append(link);
            $("#categories").append(div);
        })(category);
    }

    // Pagination
    $(".pagination").html($("#paginationTemplate").html());
    $(".current-page", ".pagination").html(data.page);
    $(".total-pages", ".pagination").html(data.pages);
    if (data.prev_link != "") {
        $(".previous-page", ".pagination").html("&laquo; Previous").attr("href", data.prev_link);
    }
    if (data.next_link != "") {
        $(".next-page", ".pagination").html("Next &raquo;").attr("href", data.next_link);
    }
    $(".order-links", ".pagination").each(function() {
        var formatted = [];
        for (var i = 0; i < data.order_links.length; i++) {
            var order_link = data.order_links[i];
            if (order_link[0] != window.location.pathname) {
                formatted.push("<a href='" + order_link[0] + "'>" + order_link[1] + "</a>");
            } else {
                formatted.push("<b>*" + order_link[1] + "</b>");
            }
        }

        $(this).append(formatted.join("; "));
    });
    for (var i = 0; i < data.order_links.length; i++) {
        var order_link = data.order_links[i];
        if (order_link[0] == window.location.pathname) {
            $("title").html($("title").html() + ": " + order_link[1] + ", page " + data.page)
        }
    }
}

google.charts.load('current', {
    'packages': ['geochart'],
    'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
});

(function($) {
    $(document).ready(function() {
        var chart_div = $('#chart_div');
        $.getJSON("/api/v1/categories", function(data) {
            $.each(data, function(item) {
                $("#categories").append($("<option>").val(this.id).text(this.name));
            });
        });
        $("#categories").change(function() {
            var selected_category = $("#categories").val();
            if(selected_category) {
                chart_div.hide();
                $.getJSON("/api/v1/category/" + selected_category, {
                })
                .done(function(data) {
                    chart_div.show();
                    data = [['Country', 'Score']].concat(data);
                    data = google.visualization.arrayToDataTable(data);
                    var chart = new google.visualization.GeoChart(chart_div[0]);
                    chart.draw(data, {});
                })
            }
            else {
                chart_div.hide();
            }
        });
    });
})(jQuery);

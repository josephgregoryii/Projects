$(document).ready(function(){

    const table = {
        'smart'         : 0,
        'creative'      : 1,
        'attractive'    : 2,
        'dependable'    : 3, 
        'social'        : 4, 
        'insecure'      : 5, 
        'cooperative'   : 6
    }

    $.ajax({
        type: "POST",
        url: "../../proxy/my-feedback.php",
        data: {"user_id" : $.cookie("user_id")},
        datatype: JSON,
        success: function(data) {
            if (data.error){
                //todo
            }
            else{
                $.each(data.feedback, function(key, value){
                    let cur_trait = data.feedback[key].trait_name;
                    let cur_trait_avg_rating   = Number(data.feedback[key].avg_rating);
                    let cur_trait_num_rating = Number(data.feedback[key].num_ratings);
                    if (table.hasOwnProperty(cur_trait)){
                        $(`#avg_rating${table[cur_trait]}`).html(`${value.avg_rating}`); 
                        $(`#num_ratings${table[cur_trait]}`).html(`${value.num_ratings}`); 
                    }
                 })
                createFeedbackList(data.feedback, getData(data.all_feedback));
            }
        },
        error: function(data){
            ;

        },
        complete: function(){
           ; 
        },
    });
    
    function getData(data){
        var statistics = { 
            1: {"ratings" : 0,
                "raw"     : 0,},
            2: {"ratings" : 0,
                "raw"     : 0},
            3: {"ratings" : 0,
                "raw"     : 0},
            4: {"ratings" : 0,
                "raw"     : 0},
            5: {"ratings" : 0,
                "raw"     : 0},
            6: {"ratings" : 0,
                "raw"     : 0},
            7: {"ratings" : 0,
                "raw"     : 0},
            "total_rates" : 0
        };

        var count = 0;
        $.each(data, function(key,value){
            statistics[value.trait_id].ratings += Number(value.num_ratings);
            statistics.total_rates += Number(value.num_ratings);
            statistics[value.trait_id].raw     += (Number(value.avg_rating) * Number(value.num_ratings));
        })
        var pop_ratings = new Array(7);
        var num_ratings = new Array(7);
        for (var i = 0; i < 7; i++){
            let avg = Number((statistics[i+1].raw / statistics[i+1].ratings).toFixed(2));
            pop_ratings[i] = avg;
            num_ratings[i] = statistics[i+1].ratings;
        }
        var result = [pop_ratings, num_ratings];

        return result;
    }

    function createFeedbackList(data, data2){
        let n = Object.keys(data).length;

        var avg_ratings = new Array(7).fill(0);
        var num_ratings = new Array(7).fill(0);
        var pop_ratings = new Array(7).fill(0);
        var pop_nums    = new Array(7).fill(0);

        for (let i=0; i < n; i++){
            let cur_trait = data[i].trait_name;
            let cur_trait_avg_rating   = Number(data[i].avg_rating);
            let cur_trait_num_rating = Number(data[i].num_ratings);

            if (cur_trait in table){
                avg_ratings[table[cur_trait]] = cur_trait_avg_rating; 
                num_ratings[table[cur_trait]] = cur_trait_num_rating; 
                pop_ratings[table[cur_trait]] = data2[0][i];
                pop_nums[table[cur_trait]]  = data2[1][i];

            }
            if(!(cur_trait in table)){
                pop_ratings[table[cur_trait]] = 0;
            }
        }

        displayGraph(avg_ratings, num_ratings, pop_ratings, pop_nums);


    }

    function displayGraph(avg_ratings, num_ratings, pop_ratings, pop_nums) {
        var ctx = document.getElementById("bar-chart").getContext("2d");
        var chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: [
                        `Smart [${num_ratings[0]}, ${pop_nums[0]}]`,
                        `Creative [${num_ratings[1]}, ${pop_nums[1]}]`,
                        `Attractive [${num_ratings[2]}, ${pop_nums[2]}]`,
                        `Dependable [${num_ratings[3]}, ${pop_nums[3]}]`,
                        `Social [${num_ratings[4]}, ${pop_nums[4]}]`,
                        `Insecure [${num_ratings[5]}, ${pop_nums[5]}]`,
                        `Cooperative [${num_ratings[6]}, ${pop_nums[6]}]`],
                datasets: [{
                        label: 'Average Ratings',
                        data: avg_ratings,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: "Population Ratings",
                        data: pop_ratings,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth : 1

                    }] 
                },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            max : 6
                        },
                        scaleLabel : {
                            display : true,
                            labelString: "Rating"
                        }
                    }]
                }
            }
        })
    }
});
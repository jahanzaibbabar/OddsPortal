
data_table = document.getElementById("data-table")
table_body = data_table.appendChild(document.createElement('tbody'))
current_status = document.getElementById("status")
details_div = document.getElementById("details")

async function getData() {
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    let date = document.URL.substring(document.URL.length - 8)
    let url = ""
    if (isNaN(date)){
        url = 'https://www.oddsportal.com/matches/soccer/';
        selected_date = document.getElementById("match_date").children[1].firstChild
        selected_date.style.color = 'red'
    }
    else{
        url = 'https://www.oddsportal.com/matches/soccer/' + date;
        month = parseInt(date.substring(4,6))
        day = parseInt(date.substring(6,8))
        month = months[month - 1]
        dates_div = document.getElementById("match_date").children
        current_page_date = day.toString() +" " + month.toString()
        console.log(current_page_date)
        for(let i=0 ; i < dates_div.length; i++){
            if (dates_div[i].textContent == current_page_date){
                console.log(current_page_date, "passed")
               dates_div[i].firstChild.style.color = "red"
            }
       }
    }
        try {
            let res = await fetch('http://127.0.0.1:8000/urls/matches',{
                method: 'POST',
            body: JSON.stringify({'url':url})
                });
            return await res.json();
        } catch (error) {
            console.log("error");
        }
    
}

async function renderData() {
    
    current_status.innerHTML = "GETTING ALL THE MATCHES URLS..."
    let data = await getData();
    total_matches = document.createElement('span')
    console.log(data)
    total_matches.innerHTML = "Total Number of Ongoing Matches : " + data["urls"].length.toString()
    details_div.appendChild(total_matches)
    current_status.innerHTML = "GOTCHA..."
    let urls = await data["urls"]
    let row_index = 0
    current_status.innerHTML = "GETTING SINGLE MATCH DETAILS..."
    for(let i=0 ; i < urls.length ; i++){
        let keepTrying;
        do{
            try{

                fetch('http://127.0.0.1:8000/urls/odds', {
                    method: 'POST',
            body: JSON.stringify({'url':urls[i]})
                }).then(res => res.json())
            .then(res => { 
                data = res["odds"]

                if (typeof data[5] !== 'undefined'){
                    
                    console.log(data + "this is data")
                    var row = table_body.insertRow(row_index)
                    row.style.color = data[9];
                    console.log(data[9])
                    row.scope = "row"
                    var indexCell = row.insertCell(0)
                    var timeCell = row.insertCell(1)
                    var nameCell = row.insertCell(2)
                    var scoreCell = row.insertCell(3)
                    var oneOddCell = row.insertCell(4)
                    var xOddCell = row.insertCell(5)
                    var twoOddCell = row.insertCell(6)
                    var payoutCell = row.insertCell(7)
                    var openingOddCell = row.insertCell(8)
                    indexCell.innerHTML = row_index + 1
                    nameCell.innerHTML = data[0]
                    oneOddCell.innerHTML = data[1]
                    xOddCell.innerHTML = data[2]
                    twoOddCell.innerHTML = data[3]
                    openingOddCell.innerHTML = data[4]
                    timeCell.innerHTML = data[6]
                    scoreCell.innerHTML = data[7]
                    payoutCell.innerHTML = data[5]
                    row_index += 1
                }
            });
            keepTrying = false
            }catch{
                keepTrying = true
            }
        }while(keepTrying)
    }
    current_status.innerHTML = "Got All Matched Results"
}



async function get_and_load_table(url){
    fetch('http://127.0.0.1:8000/urls/odds', {
        method: 'POST',
    body: JSON.stringify({'url':url})
        }).then(res => res.json())
    .then(res => { 
        return res });
}



renderData();


function refreshPage(){
    window.location.reload()
}
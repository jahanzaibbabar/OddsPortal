
data_table = document.getElementById("data-table")
table_body = data_table.appendChild(document.createElement('tbody'))
current_status = document.getElementById("status")
details_div = document.getElementById("details")
row_index = 0

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
    try{
        if (data["urls"].length == 0){
            return renderData()
        }else{
            total_matches.innerHTML = "Total Number of Ongoing Matches : " + data["urls"].length.toString()
        }
    }
    catch{
        return renderData()
    }
    details_div.appendChild(total_matches)
    current_status.innerHTML = "GOTCHA..."
    let urls = await data["urls"]
    current_status.innerHTML = "GETTING SINGLE MATCH DETAILS..."
    match_number = document.createElement("span")
    for(let i=0 ; i < urls.length ; i++){
        set_data_to_table(urls[i],row_index)
    }
    current_status.innerHTML = "Got All Matches Results"
}


function set_data_to_table(url){
    try{
        
        fetch('http://127.0.0.1:8000/urls/odds', {
            method: 'POST',
    body: JSON.stringify({'url':url})
        }).then(res => res.json())
    .then(res => { 
        data = res["odds"]
            if (data.length === 1){
                return
            }else if(data.length === 0 || typeof data == "undefined" || data == null){
                console.log("retrying "+ url)
                return set_data_to_table(url)
            }
            details_div.appendChild(match_number)
            var row = table_body.insertRow(row_index)
            row.style.color = data[9];
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
        });
    }catch{
        console.log("data was null")
    }
}




renderData();


function refreshPage(){
    window.location.reload()
}
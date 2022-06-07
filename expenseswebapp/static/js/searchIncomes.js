const searchField = document.getElementById('searchField');
const tableOutput = document.querySelector(".table-output");
const originalTable = document.querySelector(".original-table");
const paginationContainer = document.querySelector(".pagination-container");
const noResults = document.querySelector('.no-results');
const tableOutputBody = document.querySelector('.table-output-body');
tableOutput.style.display = 'none';
noResults.style.display = 'none';

searchField.addEventListener('keyup', (e)=>{
    tableOutputBody.innerHTML = ``;
    const searchValue = e.target.value;
    if(searchValue.trim().length > 0){
        paginationContainer.style.display = 'none';
        fetch("/income/search_income/", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        }).then((res) => res.json())
        .then((data) => {
            
            originalTable.style.display = 'none';
            tableOutput.style.display = 'block';

            if(data.length === 0){
                noResults.style.display = 'block';
                tableOutput.style.display = 'none';
            }
            else{
                noResults.style.display = 'none';
                var i = 1;
                data.forEach(item => {
                    tableOutputBody.innerHTML += `<tr>
                    <td scope="row">${i}</td>
                    <td>${item.amount}</td>
                    <td>${item.source}</td>
                    <td>${item.description}</td>
                    <td>${item.date}</td>
                    <td><a href='edit_expense/${item.id}' class="btn btn-primary btn-sm">edit</a></td>
                </tr>`
                i += 1;
                });
                
            }
                
        });

    }
    else{
        tableOutput.style.display = 'none';
        originalTable.style.display = 'block';
        paginationContainer.style.display = 'block';
    }
})
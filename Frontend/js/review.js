function addli() {
    // 입력한 할일 텍스트 가져와 변수에 저장
    var litext = document.getElementById("inputbox").value;

    // 새로운 리스트 생성
    var li = document.createElement("li");
    li.textContent = litext;

    // 리스트에 입력받은 텍스트 추가
    var todolist = document.getElementById("myli");
    todolist.appendChild(li);

    // input에 텍스트 입력후 입력창 비우기
    inputbox.value = '';

    // 삭제버튼 생성
    var deletebutton = document.createElement("button");
    deletebutton.textContent = "X";
    deletebutton.classList.add("deletebtn");

    // 리스트 삭제 버튼 추가
    li.appendChild(deletebutton);

    // 삭제 버튼 클릭시 해당 리스트 삭제
    deletebutton.addEventListener("click", function() {
        li.remove(); 
    });

    // 체크박스 추가, 체크박스 클릭시 취소선 생성
    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.addEventListener("change", function() {
        if (this.checked) {
            li.classList.add("completed");
            li.style.textDecoration = "line-through";
        } else {
            li.classList.remove("completed");
            li.style.textDecoration = "none";
        }
    });

    // 리스트 생성될 때마다 체크박스도 같이 생성
    li.appendChild(checkbox);
}

function goBack() {
    window.location.href = "detail.html";
  }
  
  function goReview() {
    window.location.href = "detail.html";
  }
  
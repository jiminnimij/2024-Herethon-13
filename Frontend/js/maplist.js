function goToDetail() {
  window.location.href = "detail.html";
}

function goToGood() {
  window.location.href = "detail.html";
}

function goToMap() {
  window.location.href = "maplist.html";
}

function goToCommunityl() {
  window.location.href = "detail.html";
}

function goToMy() {
  window.location.href = "detail.html";
}

// API 요청 시 인증 헤더 추가
function fetchWomenOnlyPlaces(categoryName) {
  // const accessToken = localStorage.getItem('access');
  // if (!accessToken) {
  //     alert('로그인이 필요합니다.');
  //     return;
  // }

  fetch(`http://your-backend-url/womenonly/place/?women_only_category=${categoryName}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.status === 401) {
        // 토큰이 만료된 경우 처리
        alert("인증이 필요합니다. 다시 로그인 해주세요.");
      } else {
        return response.json();
      }
    })
    .then((data) => {
      // 데이터를 가지고 지도를 업데이트하는 로직
      console.log(data);
      // 예시로 data에 따라 지도에 마커 표시
      if (data) {
        removeMarker();
        data.forEach((place) => displayMarker(place));
      }
    });
}

// 초기화 함수
function init() {
  // 로그인 예시
  login("your_username", "your_password");

  // 예시로 카테고리 검색 함수 호출
  searchCategory("GYM"); // 카테고리 코드를 실제로 사용할 코드로 대체하세요
}

window.onload = init;

const femaleBtn = document.getElementById("gender-woman");
femaleBtn.addEventListener("click", click_gender);
const maleBtn = document.getElementById("gender-man");
maleBtn.addEventListener("click", click_gender);
const noneBtn = document.getElementById("gender-none");
noneBtn.addEventListener("click", click_gender);

const agreeAllBtn = document.getElementById("TermsAgreeAll");
const requiredBtn = document.getElementById("RequiredTermsCondition");
const privacyBtn = document.getElementById("RequiredTermsOfPrivacy");


function click_gender() {
    const femaleOutCircle = document.querySelector("#gender-woman + .radioOutCircleClick");
    const maleOutCircle = document.querySelector("#gender-man + .radioOutCircleClick");
    const noneOutCircle = document.querySelector("#gender-none + .radioOutCircleClick");

    // 선택된 상태일 때 background-color 값을 변경
    if (femaleBtn.checked) {
        femaleOutCircle.style.backgroundColor = "rgb(0, 70, 42)";
    } else {
        femaleOutCircle.style.backgroundColor = "white";
    }

    if (maleBtn.checked) {
        maleOutCircle.style.backgroundColor = "rgb(0, 70, 42)";
    } else {
        maleOutCircle.style.backgroundColor = "white";
    }

    if (noneBtn.checked) {
        noneOutCircle.style.backgroundColor = "rgb(0, 70, 42)";
    } else {
        noneOutCircle.style.backgroundColor = "white";
    }
}

// 페이지 로드 시 기본 선택된 버튼 상태에 따라 background-color 설정
window.addEventListener('load', function () {
    click_gender();  // 페이지 로드 시 기본 상태에 맞게 background-color 적용
});

// 체크박스 이미지 변경 함수
function updateCheckboxImage(checkboxId, imageId) {
    const checkbox = document.getElementById(checkboxId);
    const image = document.getElementById(imageId);
    image.src = checkbox.checked ? "../static/images/체크박스2.png" : "../static/images/체크박스1.png";
}

// TermsAgreeAll 상태 업데이트 함수
function updateTermsAgreeAllState() {
    const conditionChecked = requiredBtn.checked;
    const privacyChecked = privacyBtn.checked;

    // 두 체크박스가 모두 체크되면 TermsAgreeAll 체크
    agreeAllBtn.checked = conditionChecked && privacyChecked;

    // TermsAgreeAll 상태에 맞는 이미지 업데이트
    updateCheckboxImage("TermsAgreeAll", "TermsAgreeAllImg");
}

// 각 체크박스 상태 변경 시 이미지 업데이트 및 TermsAgreeAll 상태 체크
function handleCheckboxChange() {
    // 이미지 업데이트
    updateCheckboxImage(this.id, this.id + "Img");

    // TermsAgreeAll 상태 업데이트
    updateTermsAgreeAllState();
}

// TermsAgreeAll 체크박스 클릭 시 모든 체크박스 상태 동기화
agreeAllBtn.addEventListener("change", function () {
    const isChecked = this.checked;
    requiredBtn.checked = isChecked;
    privacyBtn.checked = isChecked;

    // 이미지 업데이트
    updateCheckboxImage("TermsAgreeAll", "TermsAgreeAllImg");
    updateCheckboxImage("RequiredTermsCondition", "RequiredTermsConditionImg");
    updateCheckboxImage("RequiredTermsOfPrivacy", "RequiredTermsOfPrivacyImg");
});

// 개별 체크박스의 상태 변경 시 이미지 업데이트 및 TermsAgreeAll 상태 확인
requiredBtn.addEventListener("change", handleCheckboxChange);
privacyBtn.addEventListener("change", handleCheckboxChange);

//주소가져오기
function fetchAddress() {
    new daum.Postcode({
        oncomplete: function (data) {
            document.getElementById('address').value = data.roadAddress || data.jibunAddress;
        }
    }).open();
}

function toggleCustomDomain() {
    const emailDomain = document.getElementById("emailDomain");
    const customDomain = document.getElementById("customDomain");

    if (emailDomain.value === "custom") {
        customDomain.style.display = "inline-block";
        customDomain.required = true;
    } else {
        customDomain.style.display = "none";
        customDomain.required = false;
    }
}
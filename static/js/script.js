const langResource = {
    ko : {
        sign_up: "가입하기",
        log_in : "로그인",
        log_in2 : "로그인",
        create_acc: "가입하기",
        sign_up_logo: "가입하기",
        id_label: "아이디",
        id: "아이디",
        char_limit: "6~16 글자",
        email_label: "이메일 주소",
        email: "이메일 주소",
        password_label: "빌밀번호",
        password: "빌밀번호",
        password_length: "특수 문자와 숫자를 포함해야 합니다 (8-20 글자)",
        confirm_pw_label: "비밀번호 확인",
        "confirm-password": "비밀번호 다시 입력해주세요",
        country_label : "국적",
        south_korea : "대한민국",
        malaysia : "말레이시아",
        myanmar : "미얀마",
        australia : "호주",
        sign_up_btn : "가입하기",
        // from here
        create_profile_title: "프로필 만들기",
        profile_photo_label: "프로필 사진 업로드",
        name_label: "이름",
        gender_label: "성별",
        gender_placeholder: "성별을 선택하세요",
        male_option: "남성",
        female_option: "여성",
        language_label: "언어",
        language_placeholder: "모국어를 선택하세요",
        korean_option: "한국어",
        english_option: "영어",
        city_label: "도시",
        city_placeholder: "위치를 선택하세요",
        seoul_option: "서울",
        suwon_option: "수원",
        incheon_option: "인천",
        create_button: "만들기",
    },
    en : {
        sign_up: "Sign Up",
        log_in : "Log In",
        log_in2 : "Log In",
        create_acc: "or create an account",
        sign_up_logo: "Sign Up",
        id_label: "ID",
        id: "ID",
        char_limit: "6~16 characters",
        email_label: "Email Address",
        email: "Email Address",
        password_label: "Password",
        password: "Password",
        password_length: "must include one special characters and numbers (8-20 characters)",
        confirm_pw_label: "Confirm Password",
        "confirm-password": "Confirm your password",
        country_label : "Country",
        south_korea : "South Korea",
        malaysia : "Malaysia",
        myanmar : "Myanmar",
        australia : "Australia",
        sign_up_btn : "Sign Up",
         // from here
        create_profile_title: "Create your profile",
        profile_photo_label: "Upload Profile Photo",
        name_label: "Name",
        gender_label: "Gender",
        gender_placeholder: "Choose your gender",
        male_option: "Male",
        female_option: "Female",
        language_label: "Language",
        language_placeholder: "Choose your first language",
        korean_option: "한국어",
        english_option: "English",
        city_label: "City",
        city_placeholder: "Choose your location",
        seoul_option: "Seoul",
        suwon_option: "Suwon",
        incheon_option: "Incheon",
        create_button: "Create",

    }
}

window.addEventListener("load", function() {
    document.getElementById("languageSelector").value = "en";
    updateLanguage("en");

    document.getElementById("languageSelector").addEventListener("change", function() {
        const selectedLang = this.value;
        updateLanguage(selectedLang);
    });
    });
    
    /* 딕셔너리 내 모든 key 값을 순회하며 변경하는 함수 */
    
    function updateLanguage(lang) {
        for (let key in langResource[lang]) {
            const element = document.getElementById(key);
            if (element) {
                // Check if the key is for an input placeholder
                if (element.tagName.toLowerCase() === 'input' || element.tagName.toLowerCase() === 'textarea') {
                    element.placeholder = langResource[lang][key];
                } else {
                    element.textContent = langResource[lang][key];
                }
            }
        }
    }
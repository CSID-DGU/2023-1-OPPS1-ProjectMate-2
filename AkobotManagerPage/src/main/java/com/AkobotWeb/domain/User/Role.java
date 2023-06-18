package com.AkobotWeb.domain.User;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum Role {
    /* 구글 로그인 연동 시 권한 관련 enum 클래스, 스프링 시큐리티에서 권한 코드에 항상 ROLE_이 앞에 있어야함 */
    ROLE_GUEST("ROLE_GUEST", "게스트"),
    ROLE_USER("ROLE_USER","관리자(유저)");

    private final String key;
    private final String title;

}

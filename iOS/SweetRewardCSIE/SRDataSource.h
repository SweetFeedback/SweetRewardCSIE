//
//  SRDataSource.h
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/13.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import <Foundation/Foundation.h>

extern NSString * const SRUserDefaultUserToken;
extern NSString * const SRUserDefaultUserAccount;
extern NSString * const SRUserDefaultUserPassword;

@interface SRDataSource : NSObject

@property(strong, nonatomic) NSUserDefaults *userDefaults;
@property(nonatomic) BOOL isLogin;

+ (SRDataSource *)sharedSRDataSource;
- (BOOL)createOrLoginUserAccountByAccount:(NSString *)account andPassword:(NSString *)password;
- (BOOL)logoutUserAccount;
- (NSInteger)submitWindowByWindowID:(NSInteger)windowID;
- (NSInteger)submitWindowByWindowID:(NSInteger)windowID andAction:(NSInteger)action;


@end

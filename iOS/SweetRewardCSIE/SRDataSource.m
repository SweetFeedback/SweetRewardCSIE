//
//  SRDataSource.m
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/13.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import "SRDataSource.h"
#import "AFNetworking.h"
#import "JSONKit.h"

NSString * const SRAPIdomain = @"http://disa.csie.ntu.edu.tw";

NSString * const SRUserDefaultUserToken = @"token";
NSString * const SRUserDefaultUserAccount = @"account";
NSString * const SRUserDefaultUserPassword = @"password";

NSString * const SRServerUserToken = @"token";
NSString * const SRServerUserAccount = @"account";
NSString * const SRServerUserPassword = @"password";
NSString * const SRServerGetFeedback = @"get_feedback";
NSString * const SRServerStatus = @"status";

@implementation SRDataSource

+ (SRDataSource *)sharedSRDataSource {
    static dispatch_once_t once;
    static SRDataSource *sharedDataSource;
    dispatch_once(&once, ^ {
        sharedDataSource = [[self alloc] init];
    });
    return sharedDataSource;
}

- (id)init {
    if(self = [super init]) {
        _userDefaults = [NSUserDefaults standardUserDefaults];
        
        NSString *token = [self.userDefaults valueForKey:SRUserDefaultUserToken];
        if(token != nil) {
            _isLogin = YES;
        } else {
            _isLogin = NO;
        }   
    }
    
    return self;
}

- (BOOL)createOrLoginUserAccountByAccount:(NSString *)account andPassword:(NSString *)password {
    NSString *token = [self.userDefaults valueForKey:SRUserDefaultUserToken];
    if(token != nil && self.isLogin == YES) {
        return YES;
    }

    NSString *path = @"~blt/sweetreward/php/mobile/createNewUser.php";
    NSString *requestString = [NSString stringWithFormat:@"%@/%@?account=%@&password=%@", SRAPIdomain, path, account, password];
    NSURL *jsonURL = [NSURL URLWithString:requestString];
    
    NSString *jsonString = [[NSString alloc] initWithContentsOfURL:jsonURL encoding:NSUTF8StringEncoding error:nil];
    
    NSDictionary *result = [jsonString objectFromJSONString];
    token = result[SRServerUserToken];

    [self.userDefaults setValue:token forKey:SRUserDefaultUserToken];
    [self.userDefaults setValue:account forKey:SRUserDefaultUserAccount];
    [self.userDefaults setValue:password forKey:SRUserDefaultUserPassword];
    [self.userDefaults synchronize];
    
    self.isLogin = YES;
    
    return YES;
}

- (BOOL)logoutUserAccount {
    [self.userDefaults setValue:nil forKey:SRUserDefaultUserToken];
    [self.userDefaults synchronize];
    self.isLogin = NO;
    return YES;
}


- (NSInteger)submitWindowByWindowID:(NSInteger)windowID {
    NSString *token = [self.userDefaults valueForKey:SRUserDefaultUserToken];
    
    NSString *path = @"~blt/sweetreward/php/userActionTrigger.php";
    NSString *requestString = [NSString stringWithFormat:@"%@/%@?window_id=%d&token=%@", SRAPIdomain, path, windowID, token];
    NSURL *jsonURL = [NSURL URLWithString:requestString];
    NSString *jsonString = [[NSString alloc] initWithContentsOfURL:jsonURL encoding:NSUTF8StringEncoding error:nil];
    
    
    NSDictionary *result = [jsonString objectFromJSONString];
    NSInteger status = [[result objectForKey:SRServerStatus] integerValue];
    NSInteger getFeedback = [[result objectForKey:SRServerGetFeedback] integerValue];
    
    /*
    if(getFeedback == 1)
        return 1;
    */
    
    if(status == 0)
        return 1;
    
    return -1;
}

- (NSInteger)submitWindowByWindowID:(NSInteger)windowID andAction:(NSInteger)action{
    NSString *token = [self.userDefaults valueForKey:SRServerUserToken];
    
    NSString *path = @"~blt/sweetreward/php/userActionTrigger.php";
    NSString *requestString = [NSString stringWithFormat:@"%@/%@?window_id=%d&token=%@&action=%d", SRAPIdomain, path, windowID, token, action];
    NSURL *jsonURL = [NSURL URLWithString:requestString];
    NSString *jsonString = [[NSString alloc] initWithContentsOfURL:jsonURL encoding:NSUTF8StringEncoding error:nil];
    
    
    NSDictionary *result = [jsonString objectFromJSONString];
    NSInteger status = [[result objectForKey:SRServerStatus] integerValue];
    NSInteger getFeedback = [[result objectForKey:SRServerGetFeedback] integerValue];
    
    /*
    if(getFeedback == 1)
        return 1;
    */
    
    if(status == 0)
        return 1;
    
    return -1;
}

@end

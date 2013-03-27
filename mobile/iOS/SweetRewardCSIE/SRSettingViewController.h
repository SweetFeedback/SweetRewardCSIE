//
//  SRSettingViewController.h
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/13.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface SRSettingViewController : UITableViewController <UITextFieldDelegate>

@property (strong, nonatomic) NSString *account;
@property (strong, nonatomic) NSString *password;

@end

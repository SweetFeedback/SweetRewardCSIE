//
//  SettingViewController.h
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/13.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface SettingViewController : UIViewController
@property (strong, nonatomic) IBOutlet UITextField *accountTextField;
@property (strong, nonatomic) IBOutlet UITextField *passwordTextField;
- (IBAction)submitPressed:(UIButton *)sender;

@end

//
//  SRTextViewCell.h
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/13.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import <UIKit/UIKit.h>

// cell identifier for this custom cell
//extern NSString *kCellTextView_ID;

@interface SRTextViewCell : UITableViewCell
//+ (SRTextViewCell *)createNewTextCellFromNib;

@property (weak, nonatomic) UITextView *textView;
@property (weak, nonatomic) IBOutlet UILabel *label;


@end

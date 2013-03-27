//
//  SRTextViewCell.m
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/13.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import "SRTextViewCell.h"

//NSString* kCellTextView_ID = @"cell";

@implementation SRTextViewCell

@synthesize textView;

- (id)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier
{
    self = [super initWithStyle:style reuseIdentifier:reuseIdentifier];
    if (self) {
        // Initialization code
    }
    return self;
}

- (void)setSelected:(BOOL)selected animated:(BOOL)animated
{
    [super setSelected:selected animated:animated];

    // Configure the view for the selected state
}

//Helper method to create the workout cell from a nib file...
/*
+ (SRTextViewCell*) createNewTextCellFromNib {
    NSArray* nibContents = [[NSBundle mainBundle] loadNibNamed:@"SRTextViewCell" owner:self options:nil];
    NSEnumerator *nibEnumerator = [nibContents objectEnumerator];
    SRTextViewCell* tCell = nil;
    NSObject* nibItem = nil;
    while ( (nibItem = [nibEnumerator nextObject]) != nil) {
        if ( [nibItem isKindOfClass: [SRTextViewCell class]]) {
            tCell = (SRTextViewCell*) nibItem;
            if ([tCell.reuseIdentifier isEqualToString: kCellTextView_ID])
                break; // we have a winner
            else
                tCell = nil;
        }
    }
    return tCell;
}
*/

@end

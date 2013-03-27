//
//  QRCodeScannerViewController.h
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/12.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <AVFoundation/AVFoundation.h>
#import "ZXingWidgetController.h"

@interface QRCodeScannerViewController : UIViewController <ZXingDelegate, AVAudioPlayerDelegate> {
    AVAudioPlayer *audioPlayer;
}

@property (weak, nonatomic) IBOutlet UIWebView *webView;

@property (nonatomic, retain) IBOutlet UISlider *volumeControl;
-(IBAction) playAudio;
-(IBAction) stopAudio;
-(IBAction) adjustVolume;

- (IBAction)scanPressed:(UIBarButtonItem *)sender;


@end

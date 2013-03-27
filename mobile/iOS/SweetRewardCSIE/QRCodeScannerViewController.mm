//
//  QRCodeScannerViewController.m
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/12.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import "QRCodeScannerViewController.h"
#import "QRCodeReader.h"
#import "SRDataSource.h"

@interface QRCodeScannerViewController ()

@end

@implementation QRCodeScannerViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    NSString *urlString = @"http://disa.csie.ntu.edu.tw/~blt/sweetreward";
    NSURL *url = [NSURL URLWithString:urlString];
    [self.webView loadRequest:[NSURLRequest requestWithURL:url]];
    [self createAudioPlayer];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark -
#pragma mark ZXingDelegateMethods

- (void)zxingController:(ZXingWidgetController*)controller didScanResult:(NSString *)result {
    //self->resultsToDisplay = result;
    if (self.isViewLoaded) {
        NSArray *resultComponents = [result componentsSeparatedByString:@","];
        
        NSInteger result = -1;
        NSInteger windowID = [resultComponents[0] integerValue];
        if([resultComponents count] == 1) {
            result = [[SRDataSource sharedSRDataSource] submitWindowByWindowID:windowID];
        } else if([resultComponents count] == 2 ) {
            NSInteger action = [resultComponents[1] integerValue];
            result = [[SRDataSource sharedSRDataSource] submitWindowByWindowID:windowID andAction:action];
        } else {
            NSLog(@"Unknown QRCode result");
        }
        
        if(result == 1) {
            UIAlertView *alert = [[UIAlertView alloc] initWithTitle:nil
                                                            message:@"Thank You! Go get some candies!"
                                                           delegate:self
                                                  cancelButtonTitle:@"OK"
                                                  otherButtonTitles: nil];
            [alert show];
            [self playAudio];
        } else if(result == 0) {
            UIAlertView *alert = [[UIAlertView alloc] initWithTitle:nil
                                                            message:@"Thank You! Go get some candies!"
                                                           delegate:self
                                                  cancelButtonTitle:@"OK"
                                                  otherButtonTitles: nil];
            [alert show];
            [self playAudio];
        } else {
            UIAlertView *alert = [[UIAlertView alloc] initWithTitle:nil
                                                            message:@"Please follow the rule!"
                                                           delegate:self
                                                  cancelButtonTitle:@"OK"
                                                  otherButtonTitles: nil];
            [alert show];
        }
        
    }
    [self dismissModalViewControllerAnimated:NO];
}

- (void)zxingControllerDidCancel:(ZXingWidgetController*)controller {
    [self dismissModalViewControllerAnimated:YES];
}

- (void)viewDidUnload {
    //self->resultsView = nil;
}

#pragma mark - scan button

- (IBAction)scanPressed:(UIBarButtonItem *)sender {
    if([SRDataSource sharedSRDataSource].isLogin) {
        ZXingWidgetController *widController = [[ZXingWidgetController alloc] initWithDelegate:self showCancel:YES OneDMode:NO];
        
        NSMutableSet *readers = [[NSMutableSet alloc ] init];
        
        QRCodeReader* qrcodeReader = [[QRCodeReader alloc] init];
        [readers addObject:qrcodeReader];
        widController.readers = readers;
        
        
        [self presentModalViewController:widController animated:YES];
    } else {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:nil
                                                        message:@"Pleasee login first"
                                                       delegate:self
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles: nil];
        [alert show];
    }
    
}

#pragma mark - music

- (void)createAudioPlayer {
    NSURL *url = [NSURL fileURLWithPath:[[NSBundle mainBundle]
                                         pathForResource:@"reward"
                                         ofType:@"mp3"]];
    
    NSError *error;
    audioPlayer = [[AVAudioPlayer alloc]
                   initWithContentsOfURL:url
                   error:&error];
    if (error)
    {
        NSLog(@"Error in audioPlayer: %@",
              [error localizedDescription]);
    } else {
        audioPlayer.delegate = self;
        [audioPlayer prepareToPlay];
    }
}

- (void)playAudio {
    [audioPlayer play];
}


@end

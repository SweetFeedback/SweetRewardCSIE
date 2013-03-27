//
//  SRSettingViewController.m
//  SweetRewardCSIE
//
//  Created by Che-Wei Liang on 12/12/13.
//  Copyright (c) 2012年 agents. All rights reserved.
//

#import "SRSettingViewController.h"
#import "SRDataSource.h"
#import "SRTextViewCell.h"
#import "SRSettingTextViewCell.h"

@interface SRSettingViewController ()



@end

@implementation SRSettingViewController

- (id)initWithStyle:(UITableViewStyle)style {
    self = [super initWithStyle:style];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad {
    [super viewDidLoad];

    // Uncomment the following line to preserve selection between presentations.
    // self.clearsSelectionOnViewWillAppear = NO;
 
    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
    self.account = [[SRDataSource sharedSRDataSource].userDefaults stringForKey:SRUserDefaultUserAccount];
    self.password = [[SRDataSource sharedSRDataSource].userDefaults stringForKey:SRUserDefaultUserPassword];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return 3;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell;
    
    // Configure the cell...
    NSInteger row = indexPath.row;
    
    if(row == 0) {
        SRSettingTextViewCell *textCell = [tableView dequeueReusableCellWithIdentifier:@"TextCell"];
        if(!textCell){
            textCell = [[[NSBundle mainBundle] loadNibNamed:@"SRTextViewCell" owner:self options:nil] objectAtIndex:0];
        }
        
        textCell.label.text = @"Account";
        textCell.textField.text = self.account;
        textCell.textField.delegate = self;
        [textCell setSelectionStyle:UITableViewCellSelectionStyleNone];
        
        cell = textCell;
    } else if(row == 1) {
        SRSettingTextViewCell *textCell = [tableView dequeueReusableCellWithIdentifier:@"TextCell"];
        if(!textCell){
            textCell = [[[NSBundle mainBundle] loadNibNamed:@"SRTextViewCell" owner:self options:nil] objectAtIndex:0];
        }
        
        textCell.label.text = @"Password";
        textCell.textField.text = self.password;
        textCell.textField.secureTextEntry = YES;
        textCell.textField.delegate = self;
        [textCell setSelectionStyle:UITableViewCellSelectionStyleNone];
        
        cell = textCell;
    } else if(row == 2) {
        cell = [tableView dequeueReusableCellWithIdentifier:@"ButtonCell"];
        
        if([SRDataSource sharedSRDataSource].isLogin) {
            cell.textLabel.text = @"Logout";
        } else {
            cell.textLabel.text = @"Create / Login";
        }
    } else {
        NSAssert(NO, @"table cell out of bound");
    }
    
    return cell;
}

/*
// Override to support conditional editing of the table view.
- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the specified item to be editable.
    return YES;
}
*/

/*
// Override to support editing the table view.
- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        // Delete the row from the data source
        [tableView deleteRowsAtIndexPaths:@[indexPath] withRowAnimation:UITableViewRowAnimationFade];
    }   
    else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }   
}
*/

/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath
{
}
*/

/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/

#pragma mark - UITextFieldDelegate

- (void)textFieldDidEndEditing:(UITextField *)textField {
    UITextField *accountTextField = [(SRSettingTextViewCell *)[self.tableView cellForRowAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:0]] textField];
    UITextField *passwordTextField = [(SRSettingTextViewCell *)[self.tableView cellForRowAtIndexPath:[NSIndexPath indexPathForRow:1 inSection:0]] textField];
    
    if(textField == accountTextField){
        self.account = textField.text;
    }else if(textField == passwordTextField){
        self.password = textField.text;
    }
}


- (BOOL)textFieldShouldBeginEditing:(UITextField *)textField {
    if([SRDataSource sharedSRDataSource].isLogin) {
        return NO;
    }
    return YES;
}

- (BOOL)textFieldShouldReturn:(UITextField *)textField{
    [textField resignFirstResponder];
    UITextField *accountTextField = [(SRSettingTextViewCell *)[self.tableView cellForRowAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:0]] textField];
    UITextField *passwordTextField = [(SRSettingTextViewCell *)[self.tableView cellForRowAtIndexPath:[NSIndexPath indexPathForRow:1 inSection:0]] textField];
    
    if(textField == accountTextField){
        [passwordTextField becomeFirstResponder];
    }else if(textField == passwordTextField){

    }
    
    return YES;
}

#pragma mark - Table view delegate

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    NSInteger row = indexPath.row;
    
    if(row == 2) {
        if([SRDataSource sharedSRDataSource].isLogin) {
            [[SRDataSource sharedSRDataSource] logoutUserAccount];
        } else {
            NSString *account = [(SRSettingTextViewCell *)[self.tableView cellForRowAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:0]] textField].text;
            NSString *password = [(SRSettingTextViewCell *)[self.tableView cellForRowAtIndexPath:[NSIndexPath indexPathForRow:1 inSection:0]] textField].text;
            
            self.account = account;
            self.password = password;
            
            BOOL result = [[SRDataSource sharedSRDataSource] createOrLoginUserAccountByAccount:account andPassword:password];
            if(result) {
                UIAlertView *alert = [[UIAlertView alloc] initWithTitle:nil
                                                                message:@"Login successfully!"
                                                               delegate:self
                                                      cancelButtonTitle:@"OK"
                                                      otherButtonTitles: nil];
                [alert show];
            }
        }
        [tableView reloadData];
    }
    
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
}

@end

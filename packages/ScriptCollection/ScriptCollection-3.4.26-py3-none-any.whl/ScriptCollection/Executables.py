import os
import argparse
import time
import traceback
import keyboard
from .TasksForCommonProjectStructure import TasksForCommonProjectStructure
from .ScriptCollectionCore import ScriptCollectionCore
from .GeneralUtilities import GeneralUtilities


def DotNetsign() -> int:
    parser = argparse.ArgumentParser(description='Signs a dll- or exe-file with a snk-file. Requires ilasm and ildasm as available commandline-commands.')
    parser.add_argument("dllOrExefile")
    parser.add_argument("snkfile")
    parser.add_argument("verbose", action='store_true')
    args = parser.parse_args()
    ScriptCollectionCore().dotnet_sign(args.dllOrExefile, args.snkfile, args.verbose)
    return 0


def FilenameObfuscator() -> int:
    parser = argparse.ArgumentParser(description=''''Obfuscates the names of all files in the given folder.
Caution: This script can cause harm if you pass a wrong inputfolder-argument.''')

    parser.add_argument('--printtableheadline', type=GeneralUtilities.string_to_boolean, const=True, default=True, nargs='?',
                        help='Prints column-titles in the name-mapping-csv-file')
    parser.add_argument('--namemappingfile', default="NameMapping.csv", help='Specifies the file where the name-mapping will be written to')
    parser.add_argument('--extensions', default="exe,py,sh",
                        help='Comma-separated list of file-extensions of files where this tool should be applied. Use "*" to obfuscate all')
    parser.add_argument('--inputfolder', help='Specifies the foldere where the files are stored whose names should be obfuscated', required=True)

    args = parser.parse_args()
    ScriptCollectionCore().SCFilenameObfuscator(args.inputfolder, args.printtableheadline, args.namemappingfile, args.extensions)
    return 0


def CreateISOFileWithObfuscatedFiles() -> int:
    parser = argparse.ArgumentParser(description='''Creates an iso file with the files in the given folder and changes their names and hash-values.
This script does not process subfolders transitively.''')

    parser.add_argument('--inputfolder', help='Specifies the foldere where the files are stored which should be added to the iso-file', required=True)
    parser.add_argument('--outputfile', default="files.iso", help='Specifies the output-iso-file and its location')
    parser.add_argument('--printtableheadline', default=False, action='store_true', help='Prints column-titles in the name-mapping-csv-file')
    parser.add_argument('--createnoisofile', default=False, action='store_true', help="Create no iso file")
    parser.add_argument('--extensions', default="exe,py,sh", help='Comma-separated list of file-extensions of files where this tool should be applied. Use "*" to obfuscate all')
    args = parser.parse_args()

    ScriptCollectionCore().SCCreateISOFileWithObfuscatedFiles(args.inputfolder, args.outputfile, args.printtableheadline, not args.createnoisofile, args.extensions)
    return 0


def ChangeHashOfProgram() -> int:
    parser = argparse.ArgumentParser(description='Changes the hash-value of arbitrary files by appending data at the end of the file.')
    parser.add_argument('--inputfile', help='Specifies the script/executable-file whose hash-value should be changed', required=True)
    args = parser.parse_args()
    ScriptCollectionCore().SCChangeHashOfProgram(args.inputfile)
    return 0


def CalculateBitcoinBlockHash() -> int:
    parser = argparse.ArgumentParser(description='Calculates the Hash of the header of a bitcoin-block.')
    parser.add_argument('--version', help='Block-version', required=True)
    parser.add_argument('--previousblockhash', help='Hash-value of the previous block', required=True)
    parser.add_argument('--transactionsmerkleroot', help='Hashvalue of the merkle-root of the transactions which are contained in the block', required=True)
    parser.add_argument('--timestamp', help='Timestamp of the block', required=True)
    parser.add_argument('--target', help='difficulty', required=True)
    parser.add_argument('--nonce', help='Arbitrary 32-bit-integer-value', required=True)
    args = parser.parse_args()

    args = parser.parse_args()
    GeneralUtilities.write_message_to_stdout(ScriptCollectionCore().SCCalculateBitcoinBlockHash(args.version, args.previousblockhash,
                                                                                                args.transactionsmerkleroot, args.timestamp, args.target, args.nonce))
    return 0


def Show2FAAsQRCode():

    parser = argparse.ArgumentParser(description="""Always when you use 2-factor-authentication you have the problem:
Where to backup the secret-key so that it is easy to re-setup them when you have a new phone?
Using this script is a solution. Always when you setup a 2fa you copy and store the secret in a csv-file.
It should be obviously that this csv-file must be stored encrypted!
Now if you want to move your 2fa-codes to a new phone you simply call "SCShow2FAAsQRCode 2FA.csv"
Then the qr-codes will be displayed in the console and you can scan them on your new phone.
This script does not saving the any data anywhere.

The structure of the csv-file can be viewd here:
Displayname;Website;Email-address;Secret;Period;
Amazon;Amazon.de;myemailaddress@example.com;QWERTY;30;
Google;Google.de;myemailaddress@example.com;ASDFGH;30;

Hints:
-Since the first line of the csv-file contains headlines the first line will always be ignored
-30 is the commonly used value for the period""")
    parser.add_argument('csvfile', help='File where the 2fa-codes are stored')
    args = parser.parse_args()
    ScriptCollectionCore().SCShow2FAAsQRCode(args.csvfile)
    return 0


def SearchInFiles() -> int:
    parser = argparse.ArgumentParser(description='''Searchs for the given searchstrings in the content of all files in the given folder.
This program prints all files where the given searchstring was found to the console''')

    parser.add_argument('folder', help='Folder for search')
    parser.add_argument('searchstring', help='string to look for')

    args = parser.parse_args()
    ScriptCollectionCore().SCSearchInFiles(args.folder, args.searchstring)
    return 0


def ReplaceSubstringsInFilenames() -> int:
    parser = argparse.ArgumentParser(description='Replaces certain substrings in filenames. This program requires "pip install Send2Trash" in certain cases.')

    parser.add_argument('folder', help='Folder where the files are stored which should be renamed')
    parser.add_argument('substringInFilename', help='String to be replaced')
    parser.add_argument('newSubstringInFilename', help='new string value for filename')
    parser.add_argument('conflictResolveMode', help='''Set a method how to handle cases where a file with the new filename already exits and
    the files have not the same content. Possible values are: ignore, preservenewest, merge''')

    args = parser.parse_args()

    ScriptCollectionCore().SCReplaceSubstringsInFilenames(args.folder, args.substringInFilename, args.newSubstringInFilename, args.conflictResolveMode)
    return 0


def GenerateSnkFiles() -> int:
    parser = argparse.ArgumentParser(description='Generate multiple .snk-files')
    parser.add_argument('outputfolder', help='Folder where the files are stored which should be hashed')
    parser.add_argument('--keysize', default='4096')
    parser.add_argument('--amountofkeys', default='10')

    args = parser.parse_args()
    ScriptCollectionCore().SCGenerateSnkFiles(args.outputfolder, args.keysize, args.amountofkeys)
    return 0


def OrganizeLinesInFile() -> int:
    parser = argparse.ArgumentParser(description='Processes the lines of a file with the given commands')

    parser.add_argument('file', help='File which should be transformed')
    parser.add_argument('--encoding', default="utf-8", help='Encoding for the file which should be transformed')
    parser.add_argument("--sort", help="Sort lines", action='store_true')
    parser.add_argument("--remove_duplicated_lines", help="Remove duplicate lines", action='store_true')
    parser.add_argument("--ignore_first_line", help="Ignores the first line in the file", action='store_true')
    parser.add_argument("--remove_empty_lines", help="Removes lines which are empty or contains only whitespaces", action='store_true')
    parser.add_argument('--ignored_start_character', default="", help='Characters which should not be considered at the begin of a line')

    args = parser.parse_args()
    return ScriptCollectionCore().sc_organize_lines_in_file(args.file, args.encoding,
                                                            args.sort, args.remove_duplicated_lines, args.ignore_first_line,
                                                            args.remove_empty_lines, list(args.ignored_start_character))


def CreateHashOfAllFiles() -> int:
    parser = argparse.ArgumentParser(description='Calculates the SHA-256-value of all files in the given folder and stores the hash-value in a file next to the hashed file.')
    parser.add_argument('folder', help='Folder where the files are stored which should be hashed')
    args = parser.parse_args()
    ScriptCollectionCore().SCCreateHashOfAllFiles(args.folder)
    return 0


def CreateSimpleMergeWithoutRelease() -> int:
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('repository',  help='TODO')
    parser.add_argument('sourcebranch', default="stable", help='TODO')
    parser.add_argument('targetbranch', default="master",  help='TODO')
    parser.add_argument('remotename', default=None, help='TODO')
    parser.add_argument('--remove-sourcebranch', dest='removesourcebranch', action='store_true', help='TODO')
    parser.add_argument('--no-remove-sourcebranch', dest='removesourcebranch', action='store_false', help='TODO')
    parser.set_defaults(removesourcebranch=False)
    args = parser.parse_args()
    ScriptCollectionCore().SCCreateSimpleMergeWithoutRelease(args.repository, args.sourcebranch, args.targetbranch, args.remotename, args.removesourcebranch)
    return 0


def CreateEmptyFileWithSpecificSize() -> int:
    parser = argparse.ArgumentParser(description='Creates a file with a specific size')
    parser.add_argument('name', help='Specifies the name of the created file')
    parser.add_argument('size', help='Specifies the size of the created file')
    args = parser.parse_args()
    return ScriptCollectionCore().SCCreateEmptyFileWithSpecificSize(args.name, args.size)


def ShowMissingFiles() -> int:
    parser = argparse.ArgumentParser(description='Shows all files which are in folderA but not in folder B. This program does not do any content-comparisons.')
    parser.add_argument('folderA')
    parser.add_argument('folderB')
    args = parser.parse_args()
    ScriptCollectionCore().show_missing_files(args.folderA, args.folderB)
    return 0


def ExtractPDFPages() -> int:
    parser = argparse.ArgumentParser(description='Extract pages from PDF-file')
    parser.add_argument('file', help='Input file')
    parser.add_argument('frompage', help='First page')
    parser.add_argument('topage', help='Last page')
    parser.add_argument('outputfile', help='File for the resulting PDF-document')
    args = parser.parse_args()
    ScriptCollectionCore().extract_pdf_pages(args.file, int(args.frompage), int(args.topage), args.outputfile)
    return 0


def MergePDFs() -> int:
    parser = argparse.ArgumentParser(description='Merges PDF-files')
    parser.add_argument('files', help='Comma-separated filenames')
    parser.add_argument('outputfile', help='File for the resulting PDF-document')
    args = parser.parse_args()
    ScriptCollectionCore().merge_pdf_files(args.files.split(','), args.outputfile)
    return 0


def PDFToImage() -> int:
    parser = argparse.ArgumentParser(description='Converts a PDF-document to an image')
    parser.add_argument('file', help='Input-file')
    parser.add_argument('outputfilename_without_extension', help='File for the resulting image')
    args = parser.parse_args()
    ScriptCollectionCore().pdf_to_image(args.file, args.outputfilename_without_extension)
    return 0


def KeyboardDiagnosis() -> None:
    """Caution: This function does usually never terminate"""
    keyboard.hook(__keyhook)
    while True:
        time.sleep(10)


def __keyhook(self, event) -> None:
    GeneralUtilities.write_message_to_stdout(str(event.name)+" "+event.event_type)


def GenerateThumbnail() -> int:
    parser = argparse.ArgumentParser(description='Generate thumpnails for video-files')
    parser.add_argument('file', help='Input-videofile for thumbnail-generation')
    parser.add_argument('framerate', help='', default="16")
    args = parser.parse_args()
    try:
        ScriptCollectionCore().generate_thumbnail(args.file, args.framerate)
        return 0
    except Exception as exception:
        GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback)
        return 1


def ObfuscateFilesFolder() -> int:
    parser = argparse.ArgumentParser(description='''Changes the hash-value of the files in the given folder and renames them to obfuscated names.
This script does not process subfolders transitively.
Caution: This script can cause harm if you pass a wrong inputfolder-argument.''')

    parser.add_argument('--printtableheadline', type=GeneralUtilities.string_to_boolean, const=True,
                        default=True, nargs='?', help='Prints column-titles in the name-mapping-csv-file')
    parser.add_argument('--namemappingfile', default="NameMapping.csv", help='Specifies the file where the name-mapping will be written to')
    parser.add_argument('--extensions', default="exe,py,sh",
                        help='Comma-separated list of file-extensions of files where this tool should be applied. Use "*" to obfuscate all')
    parser.add_argument('--inputfolder', help='Specifies the folder where the files are stored whose names should be obfuscated', required=True)

    args = parser.parse_args()
    ScriptCollectionCore().SCObfuscateFilesFolder(args.inputfolder, args.printtableheadline, args.namemappingfile, args.extensions)
    return 0


def HealthCheck() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    args = parser.parse_args()
    return ScriptCollectionCore().SCHealthcheck(args.file)


def BuildCodeUnit() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--codeunitfolder', required=False, default=".")
    parser.add_argument('--verbosity', required=False, default=1)
    parser.add_argument('--targetenvironment', required=False, default="Development")
    parser.add_argument('--additionalargumentsfile', required=False, default=None)
    parser.add_argument('--assume_dependent_codeunits_are_already_built', type=GeneralUtilities.string_to_boolean, const=True, default=False, nargs='?',)
    args = parser.parse_args()
    TasksForCommonProjectStructure().build_codeunit(args.codeunitfolder, int(args.verbosity), args.targetenvironment, args.additionalargumentsfile,
                                                    False, None, args.assume_dependent_codeunits_are_already_built)
    return 0


def BuildCodeUnits() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repositoryfolder', required=False, default=".")
    parser.add_argument('--verbosity', required=False, default=1)
    parser.add_argument('--targetenvironment', required=False, default="Development")
    parser.add_argument('--additionalargumentsfile', required=False, default=None)
    # TODO add option to not fail the pipeline due to runtestcases and linting if it's a patch (=if currentversion.patchnumber!=0)
    args = parser.parse_args()
    TasksForCommonProjectStructure().build_codeunits(args.repositoryfolder, int(args.verbosity), args.targetenvironment, args.additionalargumentsfile)
    return 0


def GenerateCertificateAuthority() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--subj_c', required=True)
    parser.add_argument('--subj_st', required=True)
    parser.add_argument('--subj_l', required=True)
    parser.add_argument('--subj_o', required=True)
    parser.add_argument('--subj_ou', required=True)
    parser.add_argument('--days_until_expire', required=False, default=None, type=int)
    parser.add_argument('--password', required=False, default=None)
    args = parser.parse_args()
    ScriptCollectionCore().generate_certificate_authority(os.getcwd(), args.name, args.subj_c, args.subj_st, args.subj_l, args.subj_o, args.subj_ou, args.days_until_expire, args.password)
    return 0


def GenerateCertificate() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', required=True)
    parser.add_argument('--domain', required=True)
    parser.add_argument('--subj_c', required=True)
    parser.add_argument('--subj_st', required=True)
    parser.add_argument('--subj_l', required=True)
    parser.add_argument('--subj_o', required=True)
    parser.add_argument('--subj_ou', required=True)
    parser.add_argument('--days_until_expire', required=False, default=None, type=int)
    parser.add_argument('--password', required=False, default=None)
    args = parser.parse_args()
    ScriptCollectionCore().generate_certificate(os.getcwd(), args.domain, args.filename, args.subj_c, args.subj_st,
                                                args.subj_l, args.subj_o, args.subj_ou, args.days_until_expire, args.password)
    return 0


def GenerateCertificateSignRequest() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', required=True)
    parser.add_argument('--domain', required=True)
    parser.add_argument('--subj_c', required=True)
    parser.add_argument('--subj_st', required=True)
    parser.add_argument('--subj_l', required=True)
    parser.add_argument('--subj_o', required=True)
    parser.add_argument('--subj_ou', required=True)
    args = parser.parse_args()
    ScriptCollectionCore().generate_certificate_sign_request(os.getcwd(), args.domain, args.filename, args.subj_c, args.subj_st, args.subj_l, args.subj_o, args.sub_ou)
    return 0


def SignCertificate() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--cafolder', required=True)
    parser.add_argument('--caname', required=True)
    parser.add_argument('--targetcertificate', required=True)
    parser.add_argument('--filename', required=True)
    parser.add_argument('--days_until_expire', required=False, default=None, type=int)
    args = parser.parse_args()
    ScriptCollectionCore().sign_certificate(os.getcwd(), args.cafolder, args.caname, args.targetcertificate, args.filename, args.args.days_until_expire)
    return 0

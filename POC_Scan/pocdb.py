from POC_Scan.cms.cmsmain import *
from POC_Scan.system.systemmain import *
from POC_Scan.information.informationmain import *

class pocdb_pocs:
    def __init__(self, url):
        self.url = url
        self.informationpocdict = {
            "spring boot 路径泄露":springboot_api_BaseVerify(url),
            "options方法开启":options_method_BaseVerify(url),
            "git源码泄露扫描":git_check_BaseVerify(url),
            "java配置文件文件发现":jsp_conf_find_BaseVerify(url),
            "robots文件发现":robots_find_BaseVerify(url),
            "svn源码泄露扫描":svn_check_BaseVerify(url),
            "JetBrains IDE workspace.xml文件泄露":jetbrains_ide_workspace_disclosure_BaseVerify(url),
            "apache server-status信息泄露":apache_server_status_disclosure_BaseVerify(url),
            "crossdomain.xml文件发现":crossdomain_find_BaseVerify(url),
        }
        self.cmspocdict = {
            "泛微OA downfile.php 任意文件下载漏洞":weaver_oa_filedownload_BaseVerify(url),
            "泛微OA filedownaction SQL注入":weaver_oa_download_sqli_BaseVerify(url),
            "泛微OA 数据库配置泄露":weaver_oa_db_disclosure_BaseVerify(url),
            "通达OA RCE": tongda_rce_BaseVerify(url),
            "深信服 EDR终端检测系统RCE": sanfor_edr_rce_BaseVerify(url),
            "phpok res_action_control.php 任意文件下载(需要cookies文件)":phpok_res_action_control_filedownload_BaseVerify(url),
            "phpok api.php SQL注入漏洞":phpok_api_param_sqli_BaseVerify(url),
            "phpok remote_image getshell漏洞":phpok_remote_image_getshell_BaseVerify(url),
            "phpstudy后门漏洞":phpstudy_backdoor_BaseVerify(url),
            "Discuz论坛forum.php参数message SSRF漏洞":discuz_forum_message_ssrf_BaseVerify(url),
            "Discuz X3 focus.swf flashxss漏洞":discuz_focus_flashxss_BaseVerify(url),
            "Discuz! X2.5 物理路径泄露漏洞":discuz_x25_path_disclosure_BaseVerify(url),
            "Discuz问卷调查参数orderby注入漏洞":discuz_plugin_ques_sqli_BaseVerify(url),
            "dedecms版本探测":dedecms_version_BaseVerify(url),
            "dedecms search.php SQL注入漏洞":dedecms_search_typeArr_sqli_BaseVerify(url),
            "dedecms trace爆路径漏洞":dedecms_error_trace_disclosure_BaseVerify(url),
            "dedecms download.php重定向漏洞":dedecms_download_redirect_BaseVerify(url),
            "dedecms recommend.php SQL注入":dedecms_recommend_sqli_BaseVerify(url),
            "wordpress AzonPop插件SQL注入":wordpress_plugin_azonpop_sqli_BaseVerify(url),
            "wordpress 插件shortcode0.2.3 本地文件包含":wordpress_plugin_ShortCode_lfi_BaseVerify(url),
            "wordpress插件跳转":wordpress_url_redirect_BaseVerify(url),
            "wordpress 插件WooCommerce PHP代码注入":wordpress_woocommerce_code_exec_BaseVerify(url),
            "wordpress 插件mailpress远程代码执行":wordpress_plugin_mailpress_rce_BaseVerify(url),
            "wordpress admin-ajax.php任意文件下载":wordpress_admin_ajax_filedownload_BaseVerify(url),
            "wordpress rest api权限失效导致内容注入":wordpress_restapi_sqli_BaseVerify(url),
            "wordpress display-widgets插件后门漏洞":wordpress_display_widgets_backdoor_BaseVerify(url),
            "joomla组件com_docman本地文件包含":joomla_com_docman_lfi_BaseVerify(url),
            "joomla 3.7.0 core SQL注入":joomla_index_list_sqli_BaseVerify(url),
            "phpcms digg_add.php SQL注入":phpcms_digg_add_sqli_BaseVerify(url),
            "phpcms authkey泄露漏洞":phpcms_authkey_disclosure_BaseVerify(url),
            "phpcms2008 flash_upload.php SQL注入":phpcms_flash_upload_sqli_BaseVerify(url),
            "phpcms2008 product.php 代码执行":phpcms_product_code_exec_BaseVerify(url),
            "phpcms v9.6.0 SQL注入":phpcms_v96_sqli_BaseVerify(url),
            "phpcms 9.6.1任意文件读取漏洞":phpcms_v961_fileread_BaseVerify(url),
            "phpcms v9 flash xss漏洞":phpcms_v9_flash_xss_BaseVerify(url),
            "PhpMyAdmin2.8.0.3无需登录任意文件包含导致代码执行":phpmyadmin_setup_lfi_BaseVerify(url),
        }

        self.systempocdict = {
            "libssh身份绕过漏洞(CVE-2018-10933)":libssh_bypass_auth_BaseVerify(url),
            "Tomcat代码执行漏洞(CVE-2017-12616)":tomcat_put_exec_BaseVerify(url),
            "Tomcat 幽灵猫漏洞(CVE-2020-1938)":tomcat_Ajp_lfi_BaseVerify(url),
            "nginx Multi-FastCGI Code Execution":multi_fastcgi_code_exec_BaseVerify(url),
            "weblogic blind XXE漏洞(CVE-2018-3246)":weblogic_ws_utc_xxe_BaseVerify(url),
            "weblogic SSRF漏洞(CVE-2014-4210)":weblogic_ssrf_BaseVerify(url),
            "weblogic XMLdecoder反序列化漏洞(CVE-2017-10271)":weblogic_xmldecoder_exec_BaseVerify(url),
            "weblogic 接口泄露":weblogic_interface_disclosure_BaseVerify(url),
            "php fastcgi任意文件读取漏洞":php_fastcgi_read_BaseVerify(url),
            "php expose_php模块开启":php_expose_disclosure_BaseVerify(url),
            "IIS 6.0 webdav远程代码执行漏洞(CVE-2017-7269)":iis_webdav_rce_BaseVerify(url),
            "RDP远程代码执行漏洞(CVE-2019-0708)":rdp_code_execution_BaseVerify(url),
            "SMB远程代码执行漏洞(CVE-2020-0796)": smb_code_execution_BaseVerify(url),
        }




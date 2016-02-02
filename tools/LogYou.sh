#!/bin/bash
#
# 支持 定制路径指向 
# 支持 定制同目录内多文件处理 
# 支持 定制保存时间 
# 支持 指定删除旧数据的时间 
# 支持 每天定时touch 昨天每个小时日志 
# 支持 指定备份目录，并将2天以前的旧日志move到备份目录,如果指定目录为相对路径，那么相对的点则为 -P 所指定的目录
# 支持 删除旧数据开关
# 支持 支持2种日志备份方式，按小时，按天
# 支持 apache 日志类型，只做软连接，删除旧日志；
#
# we will ~~ we will ~ log you !
# didi log rotate tool, sunnansong@diditaxi.com.cn

#set -x
exec 0</dev/null
#exec >&./$(basename ${0}).log

help_info()
{
        cat <<-EOFSTR
	Usage: $(basename ${0}) [-S] [-P] [-F] [-B] [-T] [-D] [-X] [-V|h]
	-S      Set the save days, default 7, but savedays >= 1
	-P      Set the logfile path, this is necessary, eg: -P ./log/
	-F      Set the logfile name, this is necessary, eg: cut by ',', -F test.log,test.log.wf
	-B	Set the backup path, default './'
	-D      Set the time of delete oldfile, default '00'
	-X	Set whether delete old logfile, default '1', delete old logfile, if '-X 0' never delete old logfile
	-T      Set the type of backup logfile, default 'D'; 'D|d'=day; 'H|h'=hour;
	#-M      Set the mail adress, defalut empty, never send warning mail;
	-V | h  show help and version, i.e. this page
EOFSTR
	return 0
}

## start 

if [ ${#} -eq "0" ]
then 
	help_info	
	exit 1 
fi

# 获取脚本参数
while getopts "VhS:s:P:p:F:f:T:t:D:d:B:b:X:x:A:a" Option
do
        case ${Option} in
	h | V ) help_info; exit 0;;
	S | s ) save_days=${OPTARG};;
	P | p ) logs_path=${OPTARG};;
	F | f ) logs_file=${OPTARG};;
	D | d ) del_time=${OPTARG};;
	T | t ) bak_type=${OPTARG};;
	M | m ) mail_address=${OPTARG};;
	B | b ) bak_path=${OPTARG};;
	X | x ) is_del=${OPTARG};;
	A | a ) is_apache=${OPTARG};;
	* ) continue;;
	esac
done
shift $((OPTIND - 1))

# 获取初始化变量
mail_address=${mail_address:=''}
logs_path=${logs_path} # 日志路径，必须指定
logs_file=${logs_file} # 日志文件名,必须指定
bak_path=${bak_path:='.'} # 备份日志路径，默认当前路径 ./
bak_type=${bak_type:='H'} # 获取备  方式，默认按小时
save_days=${save_days:=7} # 保存天数,默认7天
del_time=${del_time:=00} # 执行删除动作的时刻,默认00:00
is_del=${is_del:=1} # 执行删除动作,默认1为删除
is_apache=${is_apache:=0} # 是否是apache类型日志，默认不是
cur_stmp=$(date +%H) # 获取当前小时,为做删除动作获得条件
cur_time_stmp=$(date -d "0 hours ago" +%Y%m%d%H) # 获取当前小时,用来生成文件名,精确到小时
cur_day_stmp=$(date -d "0 hours ago" +%Y%m%d) # 获取当前天,用来生成文件名,精确到天
hour_time_stmp=$(date -d "1 hours ago" +%Y%m%d%H) # 用来生成文件名,精确到小时
day_time_stmp=$(date -d "1 days ago" +%Y%m%d) # 用来生成文件名,精确到天
del_stmp=$(date -d "$(( ${save_days} + 1 )) days ago" +%Y%m%d) # 用来生成要删除的文件名
day_1=$(date -d "1 days ago" +%Y%m%d) # 1天前
day_2=$(date -d "2 days ago" +%Y%m%d) # 2天前


{ [ -z ${logs_path} ] || [ -z ${logs_file} ] || [ ${save_days} -lt 1 ];} && { \
echo "Warning:-P='' or -F='' or -S<1"; echo "please check '-P | -F | -S' \! "; exit 1; }

cd ${logs_path}/ || { echo "log path not exist \! plase check '-P ${logs_path}' \! "; exit 1; }
[ ! -d ${bak_path} ] && { mkdir -p ${bak_path} || { echo "bak path can't created \! plase check '-B ${bak_path}"; exit 1; }; }

old_ifs=${IFS}
IFS=','

for file in ${logs_file}
do
	touch ${file}

	case ${bak_type} in

        D | d ) # bak_type='D'
		if [ ${is_apache} == 0 ] # 如果is_apache=0 ,则作mv操作
		then
			if [ ! -s ${file}.${day_1} ] # 如果目标文件不存在，且大小为空则进行日志备份
			then
                                touch -a ${file}
				mv -f ${file} ${file}.${day_1}
			fi
		else
			#rm -f ${file}
			ln -sf  ${file}.${cur_day_stmp} ${file}
		fi


		# 将2天前的数据备份日志全部移动到指定备份目录
		find ./ -maxdepth 1 -mmin +$(( 24 * 60 - 30 )) -a -type f -a -name "${file}.[0-9]*" | xargs -i mv {} ${bak_path}/

		if [ ${is_del} == 1 ] # 如果is_del=1 ,则作删除操作
		then
			# 找到并删除备份目录中最后修改时间久远的日志
			find ${bak_path}/ -maxdepth 1 -mmin +$(( ${save_days} * 24 * 60 - 30 )) -a -type f -a -name "${file}.[0-9]*" | xargs -i rm -rf {}
			#find ${bak_path}/ -maxdepth 1 -mmin +$(( ${save_days} * 24 * 60 - 30 )) -a -type f -a -name "${file}.[0-9]*" | xargs -i ls -l {}
		fi

	;;
        
	* ) # bak_type='H'
		if [ ${is_apache} == 0 ] # 如果is_apache=0 ,则作mv操作
		then
			if [ ! -s ${file}.${hour_time_stmp} ]
			then
				mv -f ${file} ${file}.${hour_time_stmp}
			fi
		else
			#rm -f ${file}
			ln -fs  ${file}.${cur_time_stmp} ${file}
		fi

		if [ ${cur_stmp} == ${del_time} ]
		then
			#touch ${file}.${day_1}{00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23} 
			# 将2天前的数据备份日志全部移动到指定备份目录
			find ./ -maxdepth 1 -mmin +$(( 24 * 60 - 30 )) -a -type f -a -name "${file}.[0-9]*" | xargs -i mv {} ${bak_path}/
			#find ./ -maxdepth 1 -mmin +$(( 24 * 60 - 30 )) -a -type f -a -name "${file}.[0-9]*" | xargs -i ls -l {} ${bak_path}/

			if [ ${is_del} == 1 ] 
			then

				# 找到并删除备份目录中最后修改时间久远的日志
				find ${bak_path}/ -maxdepth 1 -mmin +$(( ${save_days} * 24 * 60 - 30 )) -a -type f -a -name "${file}.[0-9]*" | xargs -i rm -rf {}
				#find ${bak_path}/ -maxdepth 1 -mmin +$(( ${save_days} * 24 * 60 - 30 )) -a -type f -a -name "${file}.[0-9]*" | xargs -i ls -l {}
			fi
		fi
	;;

	esac

IFS=${old_ifs} # 恢复IFS

done

exit 0

## end

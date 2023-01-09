import test_application_main
import result_log as result_log

def main():
    method = 'addition'
    for m1 in range(1000, 3000+1, 500):
        for parition in range(50, 10000+1, 1000):
            try:
                test_application_main.function_for_test(method, m1, m1, m1, m1, parition)
            except Exception as e:
                print('##################')
                print(e)
                print('##################')
                result_log.add_or_create_log(
                    fileName='log_error.csv',
                    fileDir='/home/ec2-user/github-cc/',
                    dict_data={f'{method}-{m1}x{m1}':{e}}
                )


if __name__ == "__main__":
    main()
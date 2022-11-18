def distribute_jobs(chains, number_of_jobs):
    ranges = dict(chains)

    for key in ranges:
        ranges[key] = ranges[key][1] - ranges[key][0] + 1

    ranges = dict(sorted(ranges.items(), key=lambda item: item[1]))

    confs_total = sum(ranges.values())
    confs_per_job = confs_total // number_of_jobs

    if confs_total % number_of_jobs != 0:
        confs_per_job += 1

    confs_left = confs_total
    jobs = []

    if confs_total <= number_of_jobs:
        for key, value in chains.items():
            for i in range(value[0], value[1] + 1):
                jobs.append((key, i, i))
        return jobs

    for key, value in ranges.items():
        if value < confs_per_job:
            jobs.append((key, chains[key][0], chains[key][1]))
            confs_left -= value
            number_of_jobs -= 1
            confs_per_job = confs_left // number_of_jobs
            if confs_left % number_of_jobs != 0:
                confs_per_job += 1
            print('confs_left', confs_left)
            print('number_of_jobs', number_of_jobs)
            print(confs_per_job)
        else:
            start = chains[key][0]
            end = chains[key][0] + confs_per_job - 1
            while start < chains[key][1]:
                if end <= chains[key][1]:
                    jobs.append((key, start, end))
                else:
                    if start + confs_per_job // 2 <= chains[key][1]:
                        jobs.append((key, start, chains[key][1]))
                    else:
                        jobs[-1] = (jobs[-1][0], jobs[-1][1], chains[key][1])
                        confs_per_job = confs_left // number_of_jobs
                start += confs_per_job
                end += confs_per_job

    return jobs
